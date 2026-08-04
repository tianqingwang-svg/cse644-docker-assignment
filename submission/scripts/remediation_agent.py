#!/usr/bin/env python3
"""
Auto-Remediation Agent for CI Failures.

Detects specific CI failure classes (such as missing module dependencies,
ImportErrors, or source bugs), proposes minimal fixes via Anthropic LLM (or deterministic fallback),
and opens a restricted GitHub Pull Request requiring human review.
"""
import os
import sys
import json
import re
import argparse
from typing import Dict, Any, Optional

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    from github import Github
except ImportError:
    Github = None


FIX_SCHEMA = {
    "type": "object",
    "properties": {
        "failure_class": {"type": "string"},
        "root_cause": {"type": "string"},
        "fix_description": {"type": "string"},
        "fixed_file_path": {"type": "string"},
        "fixed_file_content": {"type": "string"},
    },
    "required": [
        "failure_class", "root_cause", "fix_description", "fixed_file_path", "fixed_file_content"
    ],
    "additionalProperties": False,
}


def analyze_log_fallback(log_text: str) -> Optional[Dict[str, Any]]:
    """
    Rule-based deterministic engine for offline fallback / dry-runs.
    Target Failure Class: ModuleNotFoundError / ImportError.
    """
    match = re.search(r"ModuleNotFoundError: No module named ['\"]([^'\"]+)['\"]", log_text)
    if not match:
        match = re.search(r"ImportError: cannot import name ['\"]([^'\"]+)['\"]", log_text)

    if match:
        missing_module = match.group(1)
        req_path = "requirements.txt"
        existing_req = ""
        if os.path.exists(req_path):
            with open(req_path, "r") as f:
                existing_req = f.read()

        updated_req = existing_req.strip() + f"\n{missing_module}\n"
        return {
            "failure_class": "MissingDependency (ModuleNotFoundError)",
            "root_cause": f"Required Python package '{missing_module}' is not installed or missing from requirements.txt",
            "fix_description": f"Add missing package '{missing_module}' to requirements.txt",
            "fixed_file_path": "requirements.txt",
            "fixed_file_content": updated_req,
        }
    return None


def call_llm_agent(log_text: str, source_code_map: Dict[str, str], api_key: str) -> Dict[str, Any]:
    """Call Anthropic Opus/Haiku to analyze build log and produce structured fix."""
    client = anthropic.Anthropic(api_key=api_key)
    model = os.environ.get("MODEL", "claude-haiku-4-5")

    sources_str = "\n\n".join(
        [f"File `{path}`:\n```\n{content}\n```" for path, content in source_code_map.items()]
    )

    system_prompt = (
        "You are an automated CI Remediation Agent. Your job is to analyze build failure logs "
        "and propose minimal, targeted fixes. Focus on fixing missing dependencies in requirements.txt "
        "or fixing bugs in source files (under src/). NEVER modify test files under tests/ or CI configs. "
        "Return structured JSON matching the provided schema."
    )

    user_content = f"Build failure log:\n```\n{log_text}\n```\n\nExisting Source Files:\n{sources_str}"

    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system_prompt,
        output_config={"format": {"type": "json_schema", "schema": FIX_SCHEMA}},
        messages=[{"role": "user", "content": user_content}],
    )

    text_block = next(b.text for b in response.content if b.type == "text")
    return json.loads(text_block)


def open_github_pr(fix_data: Dict[str, Any], repo_name: str, base_branch: str, token: str) -> str:
    """Open GitHub Pull Request with proposed remediation fix."""
    if not Github:
        raise RuntimeError("PyGithub library not installed. Cannot open PR.")

    gh = Github(token)
    repo = gh.get_repo(repo_name)
    run_id = os.environ.get("GITHUB_RUN_ID", "local")
    branch_name = f"bot/fix-remediation-{run_id}"

    # Get SHA of base branch
    base_ref = repo.get_git_ref(f"heads/{base_branch}")
    base_sha = base_ref.object.sha

    # Create new branch
    repo.create_git_ref(f"refs/heads/{branch_name}", base_sha)

    # Get file SHA if it exists
    file_path = fix_data["fixed_file_path"]
    try:
        file_contents = repo.get_contents(file_path, ref=base_branch)
        sha = file_contents.sha
    except Exception:
        sha = None

    commit_msg = f"[bot] fix: {fix_data['fix_description'][:72]}"

    if sha:
        repo.update_file(file_path, commit_msg, fix_data["fixed_file_content"], sha, branch=branch_name)
    else:
        repo.create_file(file_path, commit_msg, fix_data["fixed_file_content"], branch=branch_name)

    pr = repo.create_pull(
        title=f"[Bot Remediation] {fix_data['root_cause'][:60]}",
        body=(
            f"## 🤖 Auto-Remediation Proposed Fix\n\n"
            f"**Failure Class:** `{fix_data['failure_class']}`\n\n"
            f"**Root Cause:** {fix_data['root_cause']}\n\n"
            f"**Proposed Change:** {fix_data['fix_description']}\n\n"
            f"---\n"
            f"### 🛡️ Human Reviewer Checklist\n"
            f"- [ ] Proposed fix directly addresses the root cause\n"
            f"- [ ] No unintended modifications to tests or pipeline configs\n"
            f"- [ ] Blast radius is minimal and scoped\n\n"
            f"*This PR was opened automatically by the Build Remediation Agent. "
            f"A human reviewer must approve and merge this PR.*"
        ),
        head=branch_name,
        base=base_branch,
    )
    return pr.html_url


def main():
    parser = argparse.ArgumentParser(description="CI Remediation Agent")
    parser.add_argument("--log", default="build_log.txt", help="Path to build log file")
    parser.add_argument("--dry-run", action="store_true", help="Print proposed fix without opening GitHub PR")
    args = parser.parse_args()

    if not os.path.exists(args.log):
        print(f"❌ Log file not found: {args.log}")
        sys.exit(1)

    with open(args.log, "r", encoding="utf-8", errors="ignore") as f:
        log_text = f.read()

    # Collect source files for context
    sources = {}
    for root, _, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file).replace("\\", "/")
                with open(path, "r", encoding="utf-8") as f:
                    sources[path] = f.read()

    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as f:
            sources["requirements.txt"] = f.read()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    fix_data = None

    if api_key and anthropic:
        try:
            print("🤖 Calling Anthropic LLM Remediation Agent...")
            fix_data = call_llm_agent(log_text, sources, api_key)
        except Exception as e:
            print(f"⚠️ LLM Call failed ({e}), falling back to deterministic analysis engine.")

    if not fix_data:
        print("🔍 Running Rule-Engine Fallback Analyzer...")
        fix_data = analyze_log_fallback(log_text)

    if not fix_data:
        print("❌ Could not determine automated fix for this failure class.")
        sys.exit(1)

    print("\n================ 🤖 AGENT REMEDIATION PROPOSAL ================")
    print(f"Failure Class   : {fix_data['failure_class']}")
    print(f"Root Cause      : {fix_data['root_cause']}")
    print(f"Fix Description : {fix_data['fix_description']}")
    print(f"Target File     : {fix_data['fixed_file_path']}")
    print("---------------- Proposed File Content ----------------")
    print(fix_data["fixed_file_content"])
    print("=================================================================\n")

    gh_token = os.environ.get("GH_TOKEN")
    repo_name = os.environ.get("REPO")
    base_branch = os.environ.get("BASE_BRANCH", "main")

    if args.dry-run or not (gh_token and repo_name):
        print("💡 Dry-run mode active (or GH_TOKEN/REPO not set). No PR opened.")
        sys.exit(0)

    print(f"🚀 Opening GitHub PR on repository '{repo_name}'...")
    pr_url = open_github_pr(fix_data, repo_name, base_branch, gh_token)
    print(f"✅ Successfully opened Pull Request: {pr_url}")


if __name__ == "__main__":
    main()
