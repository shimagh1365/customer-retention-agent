import pandas as pd
import os

BASE = "src/data/full_realistic_dataset"

files = [
    "customers.csv",
    "leases.csv",
    "payments.csv",
    "complaints.csv",
    "call_center.csv",
    "service_history.csv",
    "sales_interactions.csv"
]

print("\n🔎 Inspecting columns in all datasets:\n")

for f in files:
    path = os.path.join(BASE, f)
    df = pd.read_csv(path, encoding="utf-8-sig")
    print(f"--- {f} ---")
    print(df.columns.tolist())
    print()
