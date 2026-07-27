"""
Hugging Face Dataset Card Generator.

Generates HF-compliant Markdown Dataset Cards with explicit licensing,
intended use, limitations, sensitive attributes, potential biases, and prohibited uses.
"""

from hf_core_lab.data.analyzer import DatasetQualityReport


class DatasetCardGenerator:
    """Generator for Hugging Face Dataset Card metadata documentation."""

    @staticmethod
    def generate_card(
        dataset_name: str,
        report: DatasetQualityReport,
        license_name: str = "mit",
        author: str = "Arun Kumar Gharami",
        description: str | None = None,
    ) -> str:
        """Generate Hugging Face Dataset Card YAML frontmatter and markdown body."""
        desc = description or "Audited synthetic financial transactions dataset for risk pattern decision support."

        card_text = f"""---
language:
- en
license: {license_name}
size_categories:
- 1K<n<10K
task_categories:
- tabular-classification
tags:
- finance
- fraud-risk
- synthetic
- trustworthy-ai
pretty_name: {dataset_name}
---

# Dataset Card for {dataset_name}

## Dataset Summary

{desc}

- **Dataset Name:** `{dataset_name}`
- **Author / Maintainer:** {author}
- **Data Type:** Synthetic Tabular Data
- **Total Rows:** `{report.total_rows:,}`
- **Total Columns:** `{report.total_columns}`
- **Duplicate Rows:** `{report.duplicate_rows}` (`{report.duplicate_ratio * 100:.2f}%`)

## Dataset Structure & Class Distribution

| Class Label | Instance Count | Percentage |
| --- | --- | --- |
"""
        for cls, count in report.class_distribution.items():
            ratio = report.class_ratios.get(cls, 0.0) * 100
            card_text += f"| `{cls}` | {count:,} | {ratio:.2f}% |\n"

        card_text += """
## Ethical Use & Governance Specification

### 1. Data Source & Provenance
This dataset was generated using a controlled algorithmic synthetic generator (`SyntheticFraudDataGenerator`). It contains **zero real-world customer PII** or private financial account details.

### 2. Intended Use
Designed exclusively for educational, research, and technical decision support benchmarking in financial risk pattern detection.

### 3. Out-of-Scope & Prohibited Uses
- **DO NOT** use this dataset to train automated legal, criminal, or employment denial systems.
- **DO NOT** claim synthetic data represents real-world population distributions without empirical validation.

### 4. Sensitive Attributes & Bias Considerations
- **Demographic Variables:** No race, gender, age, or protected class features are present.
- **Channel Imbalance:** Transactions over mobile and web channels represent 75% of data.
- **Limitations:** Synthetic heuristics do not capture evolving adversary tactics.

### 5. Responsible AI Advisory Notice
> Models trained on this dataset must issue non-accusatory statistical risk advisories and function strictly under human oversight.
"""
        return card_text
