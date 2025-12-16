import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def inject_test_high_risk_customers(df):
    """
    Inject 3 truly diverse high-risk customers so UI shows different
    names, personas, reasoning, offers, and emails.
    """

    diverse_customers = [
        # Customer 1 – Urgent + Very Low Satisfaction + Missed Payments
        {
            "customer_id": "TEST-HR-750714",
            "name": "Ahmed Saleh",
            "nationality": "Egypt",
            "car_model": "MG ZS",
            "days_until_lease_end": 1,
            "missed_payments": 3,
            "complaint_count": 2,
            "avg_service_satisfaction": 1.8,
            "service_visits": 2,
            "churn_risk_bucket": "High",
            "churn_risk_score": 0.92,
            "renewal_priority": "🔥 Top Priority (Save Now)"
        },

        # Customer 2 – Complaint-Driven
        {
            "customer_id": "TEST-HR-267922",
            "name": "Priya Singh",
            "nationality": "India",
            "car_model": "MG HS",
            "days_until_lease_end": 11,
            "missed_payments": 0,
            "complaint_count": 4,
            "avg_service_satisfaction": 3.0,
            "service_visits": 5,
            "churn_risk_bucket": "High",
            "churn_risk_score": 0.81,
            "renewal_priority": "High Priority"
        },

        # Customer 3 – Financial Risk
        {
            "customer_id": "TEST-HR-181435",
            "name": "Bilal Khan",
            "nationality": "Pakistan",
            "car_model": "XPENG G9",
            "days_until_lease_end": 13,
            "missed_payments": 5,
            "complaint_count": 0,
            "avg_service_satisfaction": 4.7,
            "service_visits": 1,
            "churn_risk_bucket": "High",
            "churn_risk_score": 0.95,
            "renewal_priority": "🔥 Top Priority (Save Now)"
        }
    ]

    df = df.copy()
    test_df = pd.DataFrame(diverse_customers)

    # Fill missing columns to match master df
    for col in df.columns:
        if col not in test_df.columns:
            test_df[col] = df[col].mode()[0] if col != "customer_id" else None

    return pd.concat([df, test_df], ignore_index=True)
