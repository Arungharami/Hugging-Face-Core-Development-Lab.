# External Open-Source Contribution Candidate Blueprint

**Target Repository:** [`huggingface/huggingface_hub`](https://github.com/huggingface/huggingface_hub)  
**Author:** Arun Kumar Gharami  
**Status:** Candidate Issue & Patch Specification  

---

## 1. Candidate Issue Summary

### Issue Title
`[FR] Enhance error message specificity when ModelCard metadata fails YAML frontmatter parsing`

### Objective
When parsing model cards containing malformed YAML tags (e.g. missing colons or unquoted special characters), `huggingface_hub.ModelCard.load()` raises a generic `ValueError` without indicating the exact line number or field where parsing failed.

---

## 2. Minimal Reproduction Script (`repro_card_issue.py`)

```python
from huggingface_hub import ModelCard

# Malformed YAML frontmatter (unquoted colon in tag)
bad_card_content = """---
license: mit
tags:
- text:classification:invalid
---
# Sample Card
"""

try:
    card = ModelCard(bad_card_content)
    print("Card loaded successfully.")
except Exception as e:
    print(f"Captured Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")
```

---

## 3. Proposed Solution & Focused Patch

Update `huggingface_hub/src/huggingface_hub/repocard.py` to catch `yaml.YAMLError` and enrich the raised `ValueError` with line and column metadata:

```python
# Proposed Patch Snippet for huggingface_hub/repocard.py
try:
    data = yaml.safe_load(yaml_content)
except yaml.YAMLError as exc:
    line_info = f" at line {exc.problem_mark.line + 1}" if hasattr(exc, "problem_mark") else ""
    raise ValueError(f"Failed to parse ModelCard YAML frontmatter{line_info}: {exc}") from exc
```

---

## 4. Unit Test Addition

```python
def test_parse_invalid_yaml_frontmatter_line_number():
    bad_yaml = "---\nlicense: mit\n  invalid:yaml:syntax\n---"
    with pytest.raises(ValueError, match="at line 3"):
        ModelCard(bad_yaml)
```

---

## 5. External Pull Request Template

```markdown
## Summary
Fixes #<ISSUE_NUMBER>. Enriches ModelCard YAML parsing errors with exact line number information.

## Changes
- Updated `ModelCard` constructor in `huggingface_hub/repocard.py` to format `yaml.YAMLError` mark details.
- Added unit test in `tests/test_repocard.py`.

## Verification
- Ran `pytest tests/test_repocard.py` (Pass 100%).
```
