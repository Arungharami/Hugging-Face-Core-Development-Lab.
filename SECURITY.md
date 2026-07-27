# Security Policy & Secret Scanning Guidance

## Reporting a Vulnerability

Security is a paramount concern for the **Hugging Face Core Development Lab**. If you discover a security vulnerability or potential credential leak, please notify the maintainer directly instead of opening a public GitHub issue.

* **Primary Security Contact:** Arun Kumar Gharami
* **GitHub Profile:** [@Arungharami](https://github.com/Arungharami)

---

## Secret Protection Rules

1. **Zero Token Tolerance:** NEVER commit real Hugging Face API tokens (`hf_...`), private SSH keys, AWS/GCP credentials, or database passwords into source code, documentation, configuration files, test outputs, or Git history.
2. **Environment Variables Only:** Store all tokens in a local `.env` file (which is git-ignored). Use `.env.example` as a template with placeholder strings only (`replace_with_your_hugging_face_token`).
3. **Log Sanitization:** Ensure structured loggers and exception handlers strip authentication headers (`Authorization: Bearer ...`) before printing or writing logs to disk.
4. **Untrusted Code Execution:** Never pass `trust_remote_code=True` when loading models or datasets from the Hugging Face Hub unless the repository and authors have been thoroughly reviewed and audited.
5. **Git History Scrubbing:** If a secret is accidentally committed:
   - Immediately revoke the compromised token in Hugging Face settings.
   - Use `git-filter-repo` or BFG Repo-Cleaner to strip the secret from Git history.
   - Re-key all affected services.

---

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
