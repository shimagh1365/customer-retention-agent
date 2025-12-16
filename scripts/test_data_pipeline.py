from src.data.load import load_datasets
from src.data.clean import clean_dataset
from src.data.transform import build_master_dataset
from src.features.churn_features import add_churn_and_lease_features

BASE_PATH = r"C:\Users\-adm.shima\Desktop\project_structure\src\data\full_realistic_dataset"

def main():
    print("🔹 Loading datasets...")
    raw = load_datasets(BASE_PATH)
    for name, df in raw.items():
        print(f"{name}: {df.shape}")

    print("\n🔹 Cleaning...")
    clean = clean_dataset(raw)

    print("🔹 Building master dataset...")
    master = build_master_dataset(clean)

    print("🔹 Adding churn & lease features...")
    featured = add_churn_and_lease_features(master)

    print("\n✅ STEP 1 SUCCESS — Data pipeline finished!")
    print("Master shape:", master.shape)
    print("Featured shape:", featured.shape)

    print("\n🔍 First 5 rows:")
    print(featured.head(5))

if __name__ == "__main__":
    main()
