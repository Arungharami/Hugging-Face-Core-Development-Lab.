"""
Feature Attribution & Explainability Module.

Extracts feature importance scores and generates human-readable advisories for tabular models.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class ExplanationReport:
    """Human-readable explainability output for a single prediction."""

    risk_probability: float
    risk_category: str
    feature_attributions: dict[str, float]
    advisory: str

    def to_markdown(self) -> str:
        """Format explanation into a readable markdown report."""
        lines = [
            "### Explainable Risk Advisory Report",
            f"- **Statistical Risk Score:** `{self.risk_probability * 100:.1f}%`",
            f"- **Category:** `{self.risk_category}`",
            "",
            "#### Feature Contributions:",
        ]
        for feature, val in self.feature_attributions.items():
            lines.append(f" - **{feature}:** `{val:.2f}%`")
        lines.extend([
            "",
            "#### Advisory Note:",
            f"> {self.advisory}",
        ])
        return "\n".join(lines)


class FeatureExplainer:
    """Explainer for tabular risk classification predictions."""

    @staticmethod
    def explain_instance(
        features: dict[str, Any],
        model_coefficients: dict[str, float],
        risk_probability: float,
    ) -> ExplanationReport:
        """Generate feature attributions and advisory for a single transaction instance."""

        # Calculate relative feature attributions
        attributions: dict[str, float] = {}
        total_score = 0.0

        for key, weight in model_coefficients.items():
            val = float(features.get(key, 0.0))
            score = abs(val * weight)
            attributions[key] = score
            total_score += score

        if total_score > 0:
            attributions = {k: round((v / total_score) * 100, 2) for k, v in attributions.items()}
        else:
            attributions = {k: 0.0 for k in attributions.keys()}

        if risk_probability < 0.35:
            category = "Low Risk Tier"
            advisory = "Standard transaction pattern. Automated processing approved."
        elif risk_probability < 0.70:
            category = "Medium Risk Tier"
            advisory = "Moderate risk pattern detected. Flagged for secondary verification."
        else:
            category = "High Risk Tier"
            advisory = (
                "This transaction presents patterns associated with elevated risk and should be reviewed "
                "by an authorized human analyst."
            )

        return ExplanationReport(
            risk_probability=round(risk_probability, 4),
            risk_category=category,
            feature_attributions=attributions,
            advisory=advisory,
        )
