import pandas as pd

def validate_dataset(df, required_columns=None, name="dataset"):
    """
    Basic validation checks:
    - dataset is not empty
    - required columns exist
    - no duplicated customer_id (only for master tables)
    """

    print(f"\n🔍 Validating {name}...")

    # 1. Check empty
    if df.empty:
        print(f"❌ ERROR: {name} is empty")
    else:
        print(f"✔ {name} loaded with {len(df)} rows.")

    # 2. Check required columns
    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            print(f"❌ Missing columns in {name}: {missing}")
        else:
            print(f"✔ All required columns present in {name}.")

    # 3. Check duplicates (only for customer tables)
    if "customer_id" in df.columns:
        dup = df["customer_id"].duplicated().sum()
        if dup > 0:
            print(f"⚠ {dup} duplicate customer_id entries found in {name}.")
        else:
            print(f"✔ No duplicate customer_id in {name}.")
