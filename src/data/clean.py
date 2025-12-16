import pandas as pd
import numpy as np

def clean_dates(df, columns):
    """Convert messy strings into datetime, force errors to NaT."""
    for col in columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def clean_numeric(df, columns):
    """Convert numeric columns, replace non-numeric with NaN."""
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clean_text(df, columns):
    """Strip whitespace, unify text formatting."""
    for col in columns:
        df[col] = df[col].astype(str).str.strip().str.replace("\s+", " ", regex=True)
        df[col] = df[col].replace("nan", np.nan)
    return df


def remove_duplicates(df, subset_cols):
    """Remove duplicate customer or transaction rows."""
    return df.drop_duplicates(subset=subset_cols)


def fill_missing(df, strategy="basic"):
    """Fill missing values for simple columns."""
    if strategy == "basic":
        df = df.fillna({
            "satisfaction_score": df["satisfaction_score"].median() if "satisfaction_score" in df else None,
            "amount": df["amount"].median() if "amount" in df else None,
            "issue": "Unknown",
            "resolution": "Unknown"
        })
    return df


def normalize_car_models(df):
    """Lowercase, strip, unify spacing."""
    if "car_model" in df.columns:
        df["car_model"] = df["car_model"].astype(str).str.lower().str.replace("  ", " ")
    return df


def clean_dataset(datasets):
    """Apply cleaning pipeline to all datasets."""

    # Customers
    customers = datasets["customers"].copy()
    customers = clean_text(customers, ["name", "nationality", "segment", "acquisition_source"])
    customers = remove_duplicates(customers, ["customer_id"])

    # Leases
    leases = datasets["leases"].copy()
    leases = clean_dates(leases, ["lease_start", "lease_end"])
    leases = clean_numeric(leases, ["monthly_payment"])
    leases = normalize_car_models(leases)

    # Service
    service = datasets["service_history"].copy()
    service = clean_dates(service, ["service_date"])
    service = clean_numeric(service, ["amount_billed", "satisfaction_score"])

    # Payments
    payments = datasets["payments"].copy()
    payments = clean_dates(payments, ["payment_date"])
    payments = clean_numeric(payments, ["amount", "late_days"])

    # Complaints
    complaints = datasets["complaints"].copy()
    complaints = clean_text(complaints, ["issue", "status"])

    # Call Center
    call = datasets["call_center"].copy()
    call = clean_numeric(call, ["call_duration_min", "satisfaction_score"])
    call = clean_text(call, ["issue", "resolution", "notes"])

    # Sales
    sales = datasets["sales_interactions"].copy()
    sales = clean_dates(sales, ["interaction_date"])
    sales = clean_text(sales, ["salesperson", "interaction_type"])

    return {
        "customers": customers,
        "leases": leases,
        "service_history": service,
        "payments": payments,
        "complaints": complaints,
        "call_center": call,
        "sales_interactions": sales
    }
