import pandas as pd
from src.data.load import load_datasets
from src.data.clean import clean_dataset
from src.data.transform import build_master_dataset
from src.features.churn_features import add_churn_and_lease_features
from src.agent.engine import CustomerAgent
import os

def run_daily_agent(base_path, output_folder="output/actions"):
    """
    Runs the full agent pipeline and exports a CSV of recommended actions.
    """

    print("🔥 Starting Customer Intelligence Agent Pipeline...")

    # 1. Load
    print("📥 Loading datasets...")
    raw = load_datasets(base_path)

    # 2. Clean
    print("🧹 Cleaning datasets...")
    clean = clean_dataset(raw)

    # 3. Master dataset
    print("🔗 Building master dataset...")
    master = build_master_dataset(clean)

    # 4. Feature engineering
    print("🧠 Adding churn & lease features...")
    featured = add_churn_and_lease_features(master)

    # 5. Run the agent
    print("🤖 Running agent decision engine...")
    agent = CustomerAgent(featured)
    actions = agent.generate_daily_actions()

    # 6. Convert to DataFrame for export
    print("📄 Converting actions to DataFrame...")
    actions_df = pd.DataFrame(actions)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "daily_actions.csv")

    # 7. Save output
    print(f"💾 Saving actions to: {output_file}")
    actions_df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print("✅ Agent pipeline completed successfully!")
    return actions_df


if __name__ == "__main__":
    BASE_PATH = r"C:\Users\adm.shima\Desktop\project_structure\src\data\full_realistic_dataset"
    run_daily_agent(BASE_PATH)
# run agent placeholder