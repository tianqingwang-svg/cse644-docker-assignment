#!/usr/bin/env python3
"""
Test Impact Analysis & Smart Test Selection Script.

Analyzes modified files via git diff to determine which test files need to be run.
Skips execution or executes a targeted subset of unit tests based on file dependencies.
"""
import os
import sys
import subprocess
import argparse
from typing import List, Set


# Map source files to corresponding test files
SOURCE_TO_TEST_MAPPING = {
    "src/calculator.py": "tests/test_calculator.py",
    "src/utils.py": "tests/test_utils.py",
    "src/formatter.py": "tests/test_formatter.py",
}

ALL_TESTS = [
    "tests/test_calculator.py",
    "tests/test_utils.py",
    "tests/test_formatter.py",
]


def get_changed_files(base_ref: str = "main") -> List[str]:
    """Get list of changed files using git diff."""
    # Attempt diff against specified base branch
    commands = [
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        ["git", "diff", "--name-only", "HEAD~1"],
        ["git", "status", "--porcelain"],
    ]

    for cmd in commands:
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            output = result.stdout.strip()
            if output:
                lines = output.splitlines()
                # If git status --porcelain was used, parse status code prefix
                files = [line.split()[-1] for line in lines if line]
                return files
        except Exception:
            continue
    return []


def select_target_tests(changed_files: List[str]) -> List[str]:
    """
    Select tests based on changed files.
    - If no files or only non-code files (docs, md) changed -> return empty list (skip all).
    - If core config / shared requirements changed -> return all tests.
    - Otherwise -> map changed src files to corresponding test files.
    """
    if not changed_files:
        print("[Impact Analysis] No changed files detected. Defaulting to full test suite.")
        return ALL_TESTS

    print(f"[Impact Analysis] Changed files detected ({len(changed_files)}):")
    for f in changed_files:
        print(f"  - {f}")

    selected_tests: Set[str] = set()
    force_all = False

    for file in changed_files:
        norm_file = file.replace("\\", "/")

        # Non-code changes (documentation, metadata)
        if norm_file.endswith(".md") or norm_file.startswith("docs/"):
            continue

        # If shared dependencies or scripts changed, run full suite
        if norm_file in ["requirements.txt", "setup.py"] or norm_file.startswith("scripts/"):
            print(f"[Impact Analysis] Infrastructure/shared file changed: {norm_file}. Triggering full test suite.")
            force_all = True
            break

        # Map src -> test
        if norm_file in SOURCE_TO_TEST_MAPPING:
            selected_tests.add(SOURCE_TO_TEST_MAPPING[norm_file])
        elif norm_file.startswith("tests/"):
            selected_tests.add(norm_file)
        elif norm_file.startswith("src/"):
            print(f"[Impact Analysis] Unmapped source file modified: {norm_file}. Triggering full test suite.")
            force_all = True
            break

    if force_all:
        return ALL_TESTS

    return sorted(list(selected_tests))


def main():
    parser = argparse.ArgumentParser(description="Smart Test Selection CLI")
    parser.add_argument("--base-ref", default=os.environ.get("BASE_BRANCH", "main"), help="Base git ref for diff")
    parser.add_argument("--print-only", action="store_true", help="Print pytest args and exit without executing")
    args = parser.parse_args()

    changed = get_changed_files(args.base_ref)
    selected = select_target_tests(changed)

    if not selected:
        print("\n⚡ [Impact Analysis] Result: SKIPPED ALL TESTS (No relevant source code modified).")
        if args.print_only:
            print("")
            return
        sys.exit(0)

    print(f"\n🎯 [Impact Analysis] Executing {len(selected)}/{len(ALL_TESTS)} test suite(s):")
    for t in selected:
        print(f"  ✓ {t}")

    pytest_cmd = ["pytest"] + selected + ["--tb=short"]
    if args.print_only:
        print(" ".join(pytest_cmd))
        return

    # Run selected tests
    res = subprocess.run(pytest_cmd)
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
