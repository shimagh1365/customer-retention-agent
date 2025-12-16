import pandas as pd
from src.agent.engine import CustomerAgent

TEST_FILE = "master_featured_TEST_WITH_HIGHRISK.csv"

def main():
    print("🔹 Loading featured dataset with injected high-risk customers...")

    try:
        featured = pd.read_csv(TEST_FILE)
    except FileNotFoundError:
        print(f"❌ ERROR: {TEST_FILE} not found.")
        print("Make sure you ran debug_generate_test_high_risk.py first.")
        return

    print("🔹 Initializing agent...")
    agent = CustomerAgent(featured)

    print("🔹 Generating high-risk drafts (LLM)...")
    drafts = agent.create_sales_draft_packets()

    print(f"\nFound {len(drafts)} high-risk customers.\n")

    if not drafts:
        print("⚠ No high-risk customers found. Check if your test customers were created correctly.")
        return

    packet = drafts[0]

    print("=== CUSTOMER ===")
    print(packet["customer_id"], "-", packet["name"])
    print("Car:", packet["car_model"])
    print("Churn bucket:", packet["churn_risk_bucket"])
    print("Reason:", packet["reason"])
    print("Offer:", packet["recommended_offer"])

    print("\n=== LLM GENERATED EMAIL ===")
    print(packet["email_to_sales"])

if __name__ == "__main__":
    main()
