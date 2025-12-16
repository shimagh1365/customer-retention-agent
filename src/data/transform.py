import pandas as pd

def build_master_dataset(d):
    """
    d = cleaned datasets dictionary from STEP 3
    This function joins all tables into one master customer dataset.
    """

    customers = d["customers"]
    leases = d["leases"]
    service = d["service_history"]
    payments = d["payments"]
    complaints = d["complaints"]
    call = d["call_center"]
    sales = d["sales_interactions"]

    # -------------------------
    # 1. Aggregate service data
    # -------------------------
    service_agg = service.groupby("customer_id").agg({
        "amount_billed": "sum",
        "warranty_claim": "sum",
        "satisfaction_score": "mean",
        "service_date": "count"
    }).rename(columns={
        "amount_billed": "total_service_spend",
        "warranty_claim": "warranty_claims",
        "satisfaction_score": "avg_service_satisfaction",
        "service_date": "service_visits"
    })


    # -------------------------
    # 2. Aggregate payment data
    # -------------------------
    pay_agg = payments.groupby("customer_id").agg({
        "amount": "sum",
        "missed_payment": "sum",
        "late_days": "mean"
    }).rename(columns={
        "amount": "total_paid",
        "missed_payment": "missed_payments",
        "late_days": "avg_late_days"
    })


    # -------------------------
    # 3. Aggregate complaints
    # -------------------------
    comp_agg = complaints.groupby("customer_id").agg({
        "ticket_id": "count"
    }).rename(columns={"ticket_id": "complaint_count"})


    # -------------------------
    # 4. Aggregate call center
    # -------------------------
    call_agg = call.groupby("customer_id").agg({
        "call_duration_min": "mean",
        "satisfaction_score": "mean",
        "issue": "count"
    }).rename(columns={
        "call_duration_min": "avg_call_duration",
        "satisfaction_score": "avg_call_satisfaction",
        "issue": "call_count"
    })


    # -------------------------
    # 5. Aggregate sales interactions
    # -------------------------
    sales_agg = sales.groupby("customer_id").agg({
        "interaction_type": "count"
    }).rename(columns={"interaction_type": "sales_interactions"})


    # -------------------------
    # 6. MERGE EVERYTHING
    # -------------------------
    master = customers \
        .merge(leases, on="customer_id", how="left") \
        .merge(service_agg, on="customer_id", how="left") \
        .merge(pay_agg, on="customer_id", how="left") \
        .merge(comp_agg, on="customer_id", how="left") \
        .merge(call_agg, on="customer_id", how="left") \
        .merge(sales_agg, on="customer_id", how="left")

    # -------------------------
    # 7. Fill NaN with zeros for numeric aggregates
    # -------------------------
    fill_zero = [
        "total_service_spend", "warranty_claims", "avg_service_satisfaction",
        "service_visits", "total_paid", "missed_payments", "avg_late_days",
        "complaint_count", "avg_call_duration", "avg_call_satisfaction",
        "call_count", "sales_interactions"
    ]

    for col in fill_zero:
        if col in master.columns:
            master[col] = master[col].fillna(0)

    return master
