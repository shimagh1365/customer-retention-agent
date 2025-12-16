from src.data.load import load_datasets
from src.data.clean import clean_dataset
from src.data.transform import build_master_dataset
from src.features.churn_features import add_churn_and_lease_features
from src.agent.engine import CustomerAgent

BASE_PATH = r"C:\Users\-adm.shima\Desktop\project_structure\src\data\full_realistic_dataset"

def main():
    print("Running data pipeline...")
    raw = load_datasets(BASE_PATH)
    clean = clean_dataset(raw)
    master = build_master_dataset(clean)
    featured = add_churn_and_lease_features(master)

    print("Initializing agent...")
    agent = CustomerAgent(featured)

    print("Generating draft packets...")
    drafts = agent.create_sales_draft_packets()

    if not drafts:
        print("No high-risk packets found.")
        return

    packet = drafts[0]

    sender = "YOUR_GMAIL@gmail.com"
    salesperson = "SOME_EMAIL@gmail.com"

    print("Creating Gmail draft...")
    draft = agent.send_email_draft_to_sales(
        packet,
        salesperson_email=salesperson,
        sender_email=sender
    )

    print("Draft created successfully:")
    print(draft)

if __name__ == "__main__":
    main()
