# Agent-Optimized CI Pipeline (Week 3 Assignment)

An intelligent, self-healing CI/CD pipeline built with Python, Pytest, Anthropic Claude API, and GitHub Actions. This project implements **Smart Test Selection (Impact Analysis)** to optimize build times and an **Auto-Remediation Agent** with a mandatory **Human Approval Gate** to safely resolve CI failures.

---

## 🏗️ Architecture & Directory Structure

```text
submission/
├── README.md                 # Full project documentation & reflection
├── requirements.txt          # Project and agent dependencies
├── .github/workflows/
│   └── ci-agent.yml          # GitHub Actions workflow with Approval Gate
├── src/                      # Application source code
│   ├── __init__.py
│   ├── calculator.py
│   ├── utils.py
│   └── formatter.py
├── tests/                    # Pytest suite
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_utils.py
│   └── test_formatter.py
├── scripts/
│   ├── select_tests.py       # Task 1: Smart test selection script
│   └── remediation_agent.py  # Task 2: Auto-remediation LLM agent
└── docs/
    └── guardrails.md         # Safety policies & blast-radius rules
```

---

## ⚡ Task 1: Smart Test Selection (Test Impact Analysis)

`scripts/select_tests.py` analyzes modified files via `git diff` against `main` or previous commits and executes only the affected unit test suites.

### Test Skipping Metrics & Comparison

| Scenario | Files Modified | Tests Executed | Execution Time | Optimization |
|---|---|---|---|---|
| **Baseline (Full Suite)** | All / Infrastructure | 3 / 3 test files (10 tests) | 2.45s | Baseline (100%) |
| **Targeted Change A** | `src/calculator.py` | `tests/test_calculator.py` | 0.82s | **66.5% Faster** (Skipped 2 test suites) |
| **Targeted Change B** | `src/utils.py` | `tests/test_utils.py` | 0.79s | **67.8% Faster** (Skipped 2 test suites) |
| **Documentation Only** | `README.md` | None (Skipped) | 0.12s | **95.1% Faster** (100% skipped) |

### Key Logic
- If `src/<module>.py` is changed, only `tests/test_<module>.py` is run.
- If non-code files (`docs/`, `*.md`) are changed, test execution is completely skipped.
- If shared infrastructure files (`requirements.txt`, `scripts/`) are changed, the full test suite runs.

---

## 🤖 Task 2: Auto-Remediation Agent

`scripts/remediation_agent.py` targets build failures caused by **`ModuleNotFoundError` / `ImportError`** or missing dependencies.

### Workflow:
1. When a test stage fails, `build_log.txt` is captured as an artifact.
2. The Agent inspects the log using Anthropic Opus/Haiku (with JSON Schema constraint) or rule-engine fallback.
3. The Agent extracts the missing package or bug, updates `requirements.txt` or the target source file, and opens a GitHub Pull Request on a `bot/fix-*` branch.
4. A human reviewer is notified to inspect the PR and approve merging.

---

## 🛡️ Guardrails & Approval Gate

Detailed safety rules are documented in [`docs/guardrails.md`](docs/guardrails.md).

- **Human Approval Gate**: The GitHub Actions job `agent-remediate` specifies `environment: agent-proposed` requiring manual review.
- **No Autonomous Merges**: The Agent token (`GH_TOKEN`) lacks merge and admin privileges.
- **Blast-Radius Control**: The system prompt constrains the agent to change **at most 1 file** (source file or `requirements.txt`) and forbids touching `tests/` or `.github/`.

---

## 📝 Prompt Engineering Details

System prompt used in `scripts/remediation_agent.py`:
> *"You are an automated CI Remediation Agent. Your job is to analyze build failure logs and propose minimal, targeted fixes. Focus on fixing missing dependencies in requirements.txt or fixing bugs in source files (under src/). NEVER modify test files under tests/ or CI configs. Return structured JSON matching the provided schema."*

---

## 🪞 AI Disclosure & Reflection

### AI Disclosure
The Agent script uses Anthropic's Claude API (`claude-haiku-4-5` or `claude-opus-4-8`) with structured outputs (`output_config.format`) to guarantee schema compliance without markdown parsing failures.

### Reflection (Surprises & Failure Modes)
During testing, an initial prompt version attempted to fix a failing test by modifying `tests/test_calculator.py` (changing `assert add(2, 3) == 5` to `assert add(2, 3) == -1`) instead of fixing `src/calculator.py`. 
This highlighted the critical need for explicit negative constraints in the system prompt (*"NEVER modify test files under tests/"*) and enforced human review checklists before merging any automated PRs.
