import pandas as pd
from openai import OpenAI

client = OpenAI()

class LLMPersonaDiscovery:

    def __init__(self, model="gpt-4.1"):
        self.model = model

    def discover_personas(self, df: pd.DataFrame, sample_size=60):
        """
        Efficient LLM persona discovery using compressed statistical summary.
        """

        # --------------------------------------------
        # 1. Select only relevant behavioral columns
        # --------------------------------------------
        useful_cols = [
            "nationality",
            "age",
            "segment",
            "loyalty_tier",
            "total_amount_paid",
            "total_missed_payments",
            "total_late_days",
            "complaint_count",
            "avg_call_satisfaction",
            "num_service_visits",
            "avg_service_satisfaction",
            "num_sales_interactions",
            "successful_sales_interactions",
            "remaining_months",
            "churn_prob"
        ]

        df_small = df[useful_cols].copy()

        # --------------------------------------------
        # 2. Small sample to stay under token limits
        # --------------------------------------------
        sample = df_small.sample(n=min(sample_size, len(df_small)))

        # --------------------------------------------
        # 3. Summarize numerically (tiny token footprint)
        # --------------------------------------------
        summary = sample.describe(include="all").to_string()

        prompt = f"""
You are an automotive customer behavior expert.

Below is a statistical summary of real customer behavior data from a dealership.

DATA SUMMARY:
{summary}

Based on this summary:
- Identify 5–7 customer persona groups.
- Use patterns in payments, service, complaints, satisfaction, nationality, loyalty, churn probability, and renewal timing.

For each persona return:

- persona_name
- description
- behavioral_characteristics
- communication_tone
- renewal_motivators
- churn_triggers
- recommended_strategy
- email_style_example

IMPORTANT:
Return ONLY JSON (a list of persona objects).
"""

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You derive customer personas from dataset summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        # FIX: correct extraction for new OpenAI SDK  
        return response.choices[0].message.content
