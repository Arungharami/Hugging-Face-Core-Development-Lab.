# Hugging Face Space Deployment Guide

This document provides step-by-step instructions for deploying the **Explainable Fraud Risk Intelligence** Gradio Space application to the Hugging Face Hub.

---

## 1. Prerequisites

1. Active Hugging Face account ([@arun-gharami](https://huggingface.co/arun-gharami)).
2. Configured `HF_TOKEN` environment variable or active `hf auth login` session.
3. Verified local execution:
   ```bash
   python spaces/fraud-risk-intelligence/app.py
   ```

---

## 2. Option A: Deployment via `hf` CLI & Git Push

```bash
# 1. Create a new Gradio Space repository on the Hub
hf repos create fraud-risk-intelligence --type space --space-sdk gradio

# 2. Clone the remote Space repository
git clone https://huggingface.co/spaces/arun-gharami/fraud-risk-intelligence /tmp/fraud-space

# 3. Copy space files into the cloned repository
cp spaces/fraud-risk-intelligence/app.py /tmp/fraud-space/
cp spaces/fraud-risk-intelligence/README.md /tmp/fraud-space/
cp spaces/fraud-risk-intelligence/requirements.txt /tmp/fraud-space/

# 4. Commit and push to Hugging Face Spaces
cd /tmp/fraud-space
git add .
git commit -m "feat: deploy explainable fraud risk intelligence space"
git push origin main
```

---

## 3. Option B: Deployment via `hf upload`

```bash
# Upload local space directory directly to Hugging Face Space repo
hf upload arun-gharami/fraud-risk-intelligence ./spaces/fraud-risk-intelligence . --repo-type space
```

---

## 4. Verification

After deployment, visit your Space URL:
`https://huggingface.co/spaces/arun-gharami/fraud-risk-intelligence`
