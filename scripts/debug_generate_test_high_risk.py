import pandas as pd
import numpy as np
import uuid
import os

INPUT_FILE = "master_featured.csv"
OUTPUT_FILE = "master_featured_TEST_WITH_HIGHRISK.csv"


def generate_high_risk_customers(n=3):
    """Generate synthetic high-risk customer rows for testing."""

    high_risk_rows = []

    for i in range(n):
        cust_id = f"TEST-HR-{uuid.uuid4().hex[:8].upper()}"
        name = f"Test HighRisk Customer {i+1}"

        row = {
            "customer_id": cust_id,
            "name": name,
            "nationality": np.random.choice(["UAE", "Jordan", "Egypt", "India", "Pakistan"]),
            "age": np.random.randint(25, 55),
            "segment": np.random.choice(["Mass Market", "Retail", "Premium"]),
            "loyalty_tier": np.random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
            "email": f"{cust_id.lower()}@example.com",
            "phone": "0500000000",

            # Very high churn
            "churn_prob": 0.82,
            "churn_risk_bucket": "High",
            "churn_risk_score": 0.82,

            # Lease urgency
            "days_until_lease_end": np.random.randint(2, 20),
            "lease_expiring_30d": True,

            # Realistic signals
            "total_missed_payments": np.random.randint(1, 3),
            "late_days": np.random.randint(10, 50),
            "num_service_visits": np.random.randint(1, 6),
            "avg_service_satisfaction": round(np.random.uniform(1.5, 2.7), 2),
            "complaint_count": np.random.randint(1, 4),

            # Renewal priority forced high
            "renewal_priority": "🔥 Top Priority (Save Now)",

            # Car model samples
            "car_model": np.random.choice([
                "Audi Q5", "Skoda Kodiaq", "MG ZS", "Volkswagen Tiguan", "XPENG G9"
            ]),
        }

        high_risk_rows.append(row)

    return pd.DataFrame(high_risk_rows)


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ ERROR: {INPUT_FILE} not found.")
        return

    print(f"🔹 Loading {INPUT_FILE} ...")
    df = pd.read_csv(INPUT_FILE)

    print("🔹 Generating synthetic high-risk customers ...")
    hr_df = generate_high_risk_customers(n=3)

    print("🔹 Appending to featured dataset ...")
    final = pd.concat([df, hr_df], ignore_index=True)

    print(f"🔹 Saving output to {OUTPUT_FILE}")
    final.to_csv(OUTPUT_FILE, index=False)

    print("\n✅ DONE — File created:")
    print(f"   → {OUTPUT_FILE}")
    print(f"   → Added {len(hr_df)} high-risk test customers.\n")


if __name__ == "__main__":
    main()
