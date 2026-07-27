# Changelog

All notable changes to the **Hugging Face Core Development Lab** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-27

### Added
- **Repository Audit Report** (`docs/REPOSITORY_AUDIT.md`) documenting zero-base initialization, security policies, technical debt risks, and action plan.
- **Technical Architecture Specification** (`docs/ARCHITECTURE.md`) covering package layer interaction, Hub API wrappers, dataset workflows, and Gradio Space integration.
- **Six-Phase Project Roadmap** (`docs/ROADMAP.md`) tracking development from Hub engineering to open-source contribution.
- **Responsible AI Framework** (`docs/RESPONSIBLE_AI.md`) outlining non-accusatory fraud risk advisories, human oversight, and bias mitigation.
- **Core Python Package Skeleton (`src/hf_core_lab`)**:
  - Dataclass and Pydantic-backed configuration (`config.py`).
  - Custom exception hierarchy (`exceptions.py`).
  - Structured logging configuration (`logging_config.py`).
  - Hugging Face Hub Client wrapper with auth & exception mapping (`hub/client.py`).
  - Hub Discovery Engine for searching models, datasets, and Spaces (`hub/discovery.py`).
  - Metadata quality & card validators (`hub/validators.py`).
  - Data models for ModelInfo, DatasetInfo, SpaceInfo, and Report generation (`models/`).
  - Command-Line Interface (`cli.py`) with `hf-core-lab` executable script.
- **Runnable Example Scripts (`examples/`)**:
  - Model search, metadata validation, and report export script (`model_discovery.py`).
  - Dataset and Space discovery scripts (`dataset_discovery.py`, `space_discovery.py`).
- **Flagship Project Starter (`spaces/fraud-risk-intelligence/`)**:
  - Gradio web app starter for Explainable Fraud Risk Intelligence.
- **Mocked Unit Test Suite (`tests/unit/`)**:
  - Client, discovery, validator, and CLI test coverage.
- **CI/CD & Security Workflows (`.github/workflows/`)**:
  - GitHub Actions CI workflow for pytest, ruff linting, security scanning, and documentation link verification.
- **Developer & Security Documentation**:
  - `README.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `LICENSE`, `Makefile`, `.gitignore`, `pyproject.toml`, `.env.example`.
