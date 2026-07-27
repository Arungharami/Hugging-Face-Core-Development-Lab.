# Contributing to Hugging Face Core Development Lab

Thank you for your interest in contributing! This project is dedicated to building a production-grade learning and research laboratory for Hugging Face ecosystem engineering.

---

## Git Workflow & Branching Strategy

1. **Never commit directly to `main`.** Always create a feature branch:
   ```bash
   git checkout -b feat/your-feature-name
   git checkout -b fix/your-bug-fix
   git checkout -b docs/your-doc-update
   ```
2. **Conventional Commits:** Use structured commit messages:
   - `feat: add model card validator`
   - `test: add mocked hub client unit tests`
   - `docs: add responsible AI framework`
   - `fix: handle missing repository tags gracefully`
   - `ci: configure GitHub Actions pytest matrix`

---

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Arungharami/Hugging-Face-Core-Development-Lab.git
   cd Hugging-Face-Core-Development-Lab
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install package in editable mode with development dependencies:
   ```bash
   make setup
   ```
4. Copy environment template:
   ```bash
   cp .env.example .env
   ```

---

## Quality & Testing Guidelines

Before opening a pull request:
1. Ensure all unit tests pass:
   ```bash
   make test
   ```
2. Check test coverage:
   ```bash
   make test-cov
   ```
3. Verify linting:
   ```bash
   make lint
   ```
4. Confirm no secrets are present in your changes or branch history.

For detailed guidelines on external Hugging Face open-source contribution strategy, see [docs/CONTRIBUTION_GUIDE.md](file:///Users/arun/Documents/App%20idea/Hugging-Face-Core-Development-Lab/Hugging-Face-Core-Development-Lab./docs/CONTRIBUTION_GUIDE.md).
