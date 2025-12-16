import pandas as pd


def add_churn_and_lease_features(df):
    """
    Add numerical churn features and key lease timing metrics.
    """

    # -------------------------------------------------------
    # 1. Ensure lease dates are datetime
    # -------------------------------------------------------
    df["lease_start"] = pd.to_datetime(df["lease_start"], errors="coerce")
    df["lease_end"] = pd.to_datetime(df["lease_end"], errors="coerce")

    # Fill missing dates with a safe placeholder
    df["lease_start"].fillna(pd.Timestamp("2000-01-01"), inplace=True)
    df["lease_end"].fillna(pd.Timestamp("2000-01-01"), inplace=True)

    # -------------------------------------------------------
    # 2. Days until lease end
    # -------------------------------------------------------
    reference_date = pd.Timestamp.today()
    df["days_until_lease_end"] = (df["lease_end"] - reference_date).dt.days

    # -------------------------------------------------------
    # 3. Lease remaining months
    # -------------------------------------------------------
    df["remaining_months"] = df["days_until_lease_end"] / 30.0

    # -------------------------------------------------------
    # 4. Customer tenure
    # -------------------------------------------------------
    df["customer_tenure_days"] = (reference_date - df["lease_start"]).dt.days
    df["customer_tenure_months"] = df["customer_tenure_days"] / 30.0

    # -------------------------------------------------------
    # 5. Renewal priority logic
    # -------------------------------------------------------
    def calc_priority(row):
        d = row["days_until_lease_end"]

        if d <= 30:
            return "🔥 Top Priority (Save Now)"
        elif d <= 90:
            return "High Priority"
        elif d <= 180:
            return "Warm Priority"
        return "Low Priority"

    df["renewal_priority"] = df.apply(calc_priority, axis=1)

    # -------------------------------------------------------
    # 6. Risk bucket from churn_prob (already exists in your data)
    # -------------------------------------------------------
    def map_churn(prob):
        if prob >= 0.7:
            return "High"
        if prob >= 0.4:
            return "Medium"
        return "Low"

    df["churn_risk_bucket"] = df["churn_prob"].apply(map_churn)

    return df
