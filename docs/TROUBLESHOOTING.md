# Troubleshooting & Common Issues Guide

This guide provides resolutions for common issues encountered during Hugging Face Hub integration, local environment setup, and API interactions.

---

## Common Issues & Solutions

### 1. Authentication & Token Errors (`401 Unauthorized`)

**Symptom:**
```text
huggingface_hub.utils._errors.RepositoryNotFoundError: 401 Client Error: Unauthorized for url
```

**Cause:**
`HF_TOKEN` is missing, expired, or lacks necessary permissions for the target operation.

**Resolution:**
1. Check authentication status:
   ```bash
   hf auth whoami
   ```
2. Re-authenticate locally:
   ```bash
   hf auth login
   ```
   Or export your token into your environment:
   ```bash
   export HF_TOKEN="hf_..."
   ```

---

### 2. Rate Limiting (`429 Too Many Requests`)

**Symptom:**
API returns `429` status code during bulk discovery queries.

**Resolution:**
1. Pass an explicit `HF_TOKEN` to increase API rate limit quotas.
2. Reduce query `limit` parameter (e.g. from 100 to 20).
3. Use cached Hub calls via `HfApi` or local `huggingface_hub` caching.

---

### 3. Missing Metadata / Schema Validation Errors

**Symptom:**
`ValidationError: Model card is missing required field 'license'`.

**Resolution:**
Use `hf_core_lab.hub.validators.CardValidator` to inspect and auto-report missing metadata fields prior to repository upload.

---

### 4. Cache Path Permissions

**Symptom:**
Permission error writing to default `~/.cache/huggingface`.

**Resolution:**
Set custom cache directory via environment variable:
```bash
export HF_HOME="./.cache/huggingface"
```
