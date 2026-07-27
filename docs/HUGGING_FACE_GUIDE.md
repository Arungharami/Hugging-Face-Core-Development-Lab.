# Modern Hugging Face CLI & Hub Engineering Guide

This guide details modern Hugging Face Hub workflows using the official `hf` command-line utility.

---

## 1. Authentication Commands

```bash
# Check current logged-in identity and token scopes
hf auth whoami

# Login interactively with a User Access Token
hf auth login

# Logout and clear saved credentials
hf auth logout
```

---

## 2. Model, Dataset, and Space Operations

```bash
# List public models filtered by task or author
hf models list --author arun-gharami

# List datasets on the Hub
hf datasets list --search finance

# List Spaces on the Hub
hf spaces list --author arun-gharami
```

---

## 3. Upload & Download Workflows

```bash
# Download a model repository locally
hf download meta-llama/Llama-3.2-1B-Instruct --local-dir ./llama_model

# Upload local directory to a Hugging Face model repo
hf upload arun-gharami/my-cool-model ./my_model_files .

# Create a new repository on the Hub
hf repos create my-new-model --type model
```

---

## 4. Cache Management

```bash
# Inspect local Hugging Face cache usage
hf cache scan

# Delete selected cached revisions to free disk space
hf cache delete
```
