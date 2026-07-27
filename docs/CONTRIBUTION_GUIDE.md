# External Open-Source Contribution Strategy

This guide prepares **Arun Kumar Gharami** for contributing high-impact, professional pull requests to external Hugging Face open-source repositories (such as `huggingface/huggingface_hub`, `transformers`, `datasets`, or `gradio`).

---

## 1. The 6-Step Open-Source Contribution Lifecycle

```text
1. Discover Issue
       ↓
2. Reproduce Locally
       ↓
3. Design Focused Solution
       ↓
4. Implement & Test
       ↓
5. Create Pull Request
       ↓
6. Review & Iterate
```

---

## 2. Detailed Execution Guidelines

### Step 1: Identifying Candidate Issues
Look for issues labeled `good first issue`, `help wanted`, `documentation`, or `bug` on Hugging Face ecosystem repositories.

### Step 2: Local Reproduction
Before writing any code, create a minimal reproducible example (`repro.py`) that fails on the current `main` branch of the target repository.

### Step 3: Focused Patching
- Keep changes minimal and focused. Do not reformat unrelated code.
- Follow the repository's code style (e.g. running `ruff`, `black`, `isort`, or `make style`).

### Step 4: Unit Testing
Add unit tests that fail without your fix and pass with your fix.

### Step 5: Pull Request Preparation
Write a clear, structured PR description:
```markdown
## Summary
Fixes #<ISSUE_NUMBER>. Briefly describe what was changed and why.

## Changes
- Updated `HfApi.list_models` parameter parsing to handle missing tags cleanly.
- Added unit test in `tests/test_hf_api.py`.

## Verification
- Run `pytest tests/test_hf_api.py` locally (Output: 100% pass).
```

### Step 6: Code Review Etiquette
Respond promptly to maintainer feedback with gratitude and clear technical responses.
