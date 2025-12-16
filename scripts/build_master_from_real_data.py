import pandas as pd
from src.data.load import load_datasets
from src.features.build_master_dataset import build_master_dataset
from src.features.churn_features import add_churn_and_lease_features

def main():
    print("🔹 Loading all CSVs from full_realistic_dataset...")

    raw = load_datasets("src/data/full_realistic_dataset")
    print("Loaded datasets.")

    print("🔹 Building master dataset...")
    master = build_master_dataset(raw)
    print("Master shape:", master.shape)

    print("🔹 Adding churn & lease features...")
    featured = add_churn_and_lease_features(master)
    print("Featured dataset shape:", featured.shape)

    # Save
    featured.to_csv("src/data/full_realistic_dataset/master_featured.csv", index=False)
    print("✅ Saved to master_featured.csv")

if __name__ == "__main__":
    main()
