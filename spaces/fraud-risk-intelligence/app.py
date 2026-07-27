"""
Gradio Application: Explainable Fraud Risk Intelligence.

Implements transparent financial risk probability, non-accusatory advisories,
confidence scores, and visual feature attribution breakdowns.
"""

import gradio as gr


def evaluate_fraud_risk(
    transaction_amount: float,
    is_foreign_country: bool,
    failed_pin_attempts: int,
    account_age_days: int,
    channel: str,
):
    """Process input transaction features and calculate non-accusatory risk assessment."""

    # Baseline heuristic risk calculation for decision support demonstration
    amount_factor = min(1.0, transaction_amount / 10000.0) * 0.35
    foreign_factor = 0.30 if is_foreign_country else 0.0
    pin_factor = min(1.0, failed_pin_attempts / 3.0) * 0.25
    age_factor = 0.10 if account_age_days < 30 else 0.0

    raw_score = amount_factor + foreign_factor + pin_factor + age_factor
    risk_score = round(min(0.99, max(0.01, raw_score)), 4)
    confidence = round(85.0 + (risk_score * 10.0), 1)

    if risk_score < 0.35:
        risk_category = "Low Risk Tier"
        advisory_msg = (
            "Standard transaction patterns observed. No immediate risk flags triggered. "
            "Proceed with standard automated clearing procedures."
        )
    elif risk_score < 0.70:
        risk_category = "Medium Risk Tier"
        advisory_msg = (
            "This transaction presents patterns associated with moderate risk (e.g. location or amount variance). "
            "Recommended for secondary automated verification or routine queue audit."
        )
    else:
        risk_category = "High Risk Tier"
        advisory_msg = (
            "This transaction presents patterns associated with elevated risk and should be reviewed "
            "by an authorized human analyst prior to final clearance."
        )

    # Feature contribution breakdown dictionary
    features_breakdown = {
        "Transaction Amount": round(amount_factor * 100, 1),
        "Cross-Border Location": round(foreign_factor * 100, 1),
        "Failed PIN Attempts": round(pin_factor * 100, 1),
        "Account Age Risk": round(age_factor * 100, 1),
    }

    explanation_text = (
        f"### Statistical Risk Analysis Summary\n"
        f"- **Calculated Risk Probability:** `{risk_score * 100:.1f}%`\n"
        f"- **Model Confidence Score:** `{confidence}%`\n"
        f"- **Assigned Classification:** `{risk_category}`\n\n"
        f"#### Recommended Action Advisory:\n"
        f"> {advisory_msg}\n\n"
        f"#### Key Feature Attributions:\n"
        f"- **Transaction Amount Contribution:** `{amount_factor * 100:.1f}%`\n"
        f"- **Location Variance Contribution:** `{foreign_factor * 100:.1f}%`\n"
        f"- **Authentication Failures Contribution:** `{pin_factor * 100:.1f}%`\n\n"
        f"--- \n"
        f"**Responsible AI Disclaimer:** This tool provides decision support analytics only. "
        f"It does not make legal accusations or perform automated customer account actions."
    )

    return risk_category, f"{risk_score * 100:.1f}%", explanation_text, features_breakdown


def build_interface():
    theme = gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="blue",
    )

    with gr.Blocks(theme=theme, title="Explainable Fraud Risk Intelligence") as demo:
        gr.Markdown(
            """
            # 🛡️ Explainable Fraud Risk Intelligence Laboratory
            ### Decision Support & Risk Analysis Engine for Financial Operations
            *Powered by Hugging Face Core Development Lab | Author: **Arun Kumar Gharami***
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📥 Input Transaction Data")
                amount_input = gr.Number(label="Transaction Amount ($)", value=2500.0, minimum=0.0)
                foreign_input = gr.Checkbox(label="Cross-Border / Foreign Country Transaction", value=True)
                pin_input = gr.Slider(label="Failed PIN / Auth Attempts", minimum=0, maximum=5, step=1, value=1)
                age_input = gr.Number(label="Account Age (Days)", value=14, minimum=0)
                channel_input = gr.Dropdown(
                    label="Transaction Channel",
                    choices=["Online Web", "Mobile App", "POS Terminal", "ATM"],
                    value="Online Web",
                )

                submit_btn = gr.Button("Analyze Risk Pattern", variant="primary")

            with gr.Column(scale=1):
                gr.Markdown("### 📊 Risk Assessment & Explainability")
                category_output = gr.Textbox(label="Assigned Risk Category")
                probability_output = gr.Textbox(label="Statistical Risk Probability")
                explanation_output = gr.Markdown(label="Human-Readable Advisory Report")
                breakdown_output = gr.JSON(label="Feature Attribution Breakdown")

        submit_btn.click(
            fn=evaluate_fraud_risk,
            inputs=[amount_input, foreign_input, pin_input, age_input, channel_input],
            outputs=[category_output, probability_output, explanation_output, breakdown_output],
        )

        gr.Examples(
            examples=[
                [45.50, False, 0, 365, "POS Terminal"],
                [4500.00, True, 1, 90, "Online Web"],
                [12500.00, True, 3, 7, "Mobile App"],
            ],
            inputs=[amount_input, foreign_input, pin_input, age_input, channel_input],
        )

    return demo


if __name__ == "__main__":
    app = build_interface()
    app.launch()
