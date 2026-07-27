"""
Tabular Fraud Risk Model Trainer & Inference Engine.

Implements model training, metric evaluations (Accuracy, Precision, Recall, F1, ROC-AUC),
CPU inference latency benchmarking, and explainability integration.
"""

from dataclasses import dataclass
import time
from typing import Dict, List, Tuple
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

from hf_core_lab.exceptions import InferenceError, ValidationError
from hf_core_lab.logging_config import setup_logger
from hf_core_lab.models.explainability import ExplanationReport, FeatureExplainer

logger = setup_logger("hf_core_lab.models.fraud_risk")


@dataclass
class ModelEvaluationReport:
    """Evaluation metrics for a trained classification model."""

    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    inference_latency_ms: float

    def to_markdown(self) -> str:
        """Format metrics into a markdown evaluation table."""
        return (
            f"# Model Evaluation Summary: {self.model_name}\n\n"
            f"| Metric | Value |\n"
            f"| --- | --- |\n"
            f"| **Accuracy** | `{self.accuracy * 100:.2f}%` |\n"
            f"| **Precision** | `{self.precision * 100:.2f}%` |\n"
            f"| **Recall** | `{self.recall * 100:.2f}%` |\n"
            f"| **F1 Score** | `{self.f1 * 100:.2f}%` |\n"
            f"| **ROC-AUC** | `{self.roc_auc:.4f}` |\n"
            f"| **CPU Latency (per item)** | `{self.inference_latency_ms:.3f} ms` |\n"
        )


class FraudRiskClassifier:
    """Tabular classifier for financial risk decision support."""

    FEATURE_COLS = ["transaction_amount", "is_foreign_country", "failed_pin_attempts", "account_age_days"]
    COEFFICIENTS = {
        "transaction_amount": 0.0001,
        "is_foreign_country": 0.30,
        "failed_pin_attempts": 0.25,
        "account_age_days": -0.001,
    }

    def __init__(self, random_seed: int = 42):
        self.model = RandomForestClassifier(n_estimators=50, random_state=random_seed)
        self.is_trained = False

    def train(self, train_df: pd.DataFrame, target_col: str = "is_high_risk"):
        """Train classifier on prepared training DataFrame."""
        for col in self.FEATURE_COLS:
            if col not in train_df.columns:
                raise ValidationError(f"Missing required feature column '{col}' in training data.")

        X = train_df[self.FEATURE_COLS]
        y = train_df[target_col]

        logger.info("Training FraudRiskClassifier on %d rows...", len(train_df))
        self.model.fit(X, y)
        self.is_trained = True

    def evaluate(self, test_df: pd.DataFrame, target_col: str = "is_high_risk") -> ModelEvaluationReport:
        """Evaluate trained model performance against test DataFrame."""
        if not self.is_trained:
            raise InferenceError("Model must be trained before evaluation.")

        X = test_df[self.FEATURE_COLS]
        y_true = test_df[target_col]

        start_time = time.perf_counter()
        y_pred = self.model.predict(X)
        y_prob = self.model.predict_proba(X)[:, 1]
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        latency_per_item = round(elapsed_ms / len(test_df), 4)

        return ModelEvaluationReport(
            model_name="RandomForestFraudClassifier",
            accuracy=round(float(accuracy_score(y_true, y_pred)), 4),
            precision=round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
            recall=round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
            f1=round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
            roc_auc=round(float(roc_auc_score(y_true, y_prob)), 4) if len(set(y_true)) > 1 else 0.0,
            inference_latency_ms=latency_per_item,
        )

    def predict_instance(self, features: Dict[str, float]) -> Tuple[float, ExplanationReport]:
        """Predict risk probability and generate explanation for a single transaction."""
        df_inst = pd.DataFrame([features])
        for col in self.FEATURE_COLS:
            if col not in df_inst.columns:
                df_inst[col] = 0.0

        X = df_inst[self.FEATURE_COLS]

        if self.is_trained:
            prob = float(self.model.predict_proba(X)[0, 1])
        else:
            # Fallback heuristic calculation
            amount = features.get("transaction_amount", 0.0)
            foreign = features.get("is_foreign_country", 0.0)
            pin = features.get("failed_pin_attempts", 0.0)
            prob = min(0.99, max(0.01, (amount / 10000.0) * 0.35 + foreign * 0.30 + (pin / 3.0) * 0.25))

        explanation = FeatureExplainer.explain_instance(features, self.COEFFICIENTS, prob)
        return prob, explanation
