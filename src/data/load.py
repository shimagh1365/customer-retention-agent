import pandas as pd
import os

def load_datasets(base_path):
    """
    Load all raw CSV datasets into memory (only used for full pipeline builds).
    """
    datasets = {}

    datasets["customers"] = pd.read_csv(os.path.join(base_path, "customers.csv"), encoding="utf-8-sig")
    datasets["leases"] = pd.read_csv(os.path.join(base_path, "leases.csv"), encoding="utf-8-sig")
    datasets["service_history"] = pd.read_csv(os.path.join(base_path, "service_history.csv"), encoding="utf-8-sig")
    datasets["payments"] = pd.read_csv(os.path.join(base_path, "payments.csv"), encoding="utf-8-sig")
    datasets["complaints"] = pd.read_csv(os.path.join(base_path, "complaints.csv"), encoding="utf-8-sig")
    datasets["call_center"] = pd.read_csv(os.path.join(base_path, "call_center.csv"), encoding="utf-8-sig")
    datasets["sales_interactions"] = pd.read_csv(os.path.join(base_path, "sales_interactions.csv"), encoding="utf-8-sig")

    return datasets


def load_featured_dataset(base_path=None):
    """
    Loads FEATURED data (the one used by UI + Agent).

    For demo/testing:
        → We always load: data/featured_dataset.csv
    """
    # Force test dataset for stable demo
    if base_path is None:
        base_path = "data"

    file_path = os.path.join(base_path, "featured_dataset.csv")

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"featured_dataset.csv not found at: {file_path}\n"
            f"Make sure your 3 injected TEST-HR customers exist here."
        )

    df = pd.read_csv(file_path)

    # Normalize column names just in case
    df.columns = df.columns.str.strip().str.lower()

    return df
