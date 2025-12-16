import pandas as pd


def build_master_dataset(raw):
    """
    Build a unified master dataset from your actual Ali & Sons structure.
    All aggregations match the REAL CSV fields (no synthetic fields).
    """

    customers = raw["customers"]
    leases = raw["leases"]
    payments = raw["payments"]
    complaints = raw["complaints"]
    calls = raw["call_center"]
    service = raw["service_history"]
    sales = raw["sales_interactions"]

    # ---------------------------------------------------------------------
    # 1. Merge customers + leases
    # ---------------------------------------------------------------------
    master = customers.merge(
        leases,
        on="customer_id",
        how="left"
    )

    # ---------------------------------------------------------------------
    # 2. Payments Aggregation
    # ---------------------------------------------------------------------
    # Fields available: amount, missed_payment, late_days
    payments_agg = payments.groupby("customer_id").agg({
        "amount": "sum",
        "missed_payment": "sum",
        "late_days": "sum"
    }).reset_index()

    payments_agg.rename(columns={
        "amount": "total_amount_paid",
        "missed_payment": "total_missed_payments",
        "late_days": "total_late_days"
    }, inplace=True)

    master = master.merge(payments_agg, on="customer_id", how="left")

    # ---------------------------------------------------------------------
    # 3. Complaints Aggregation
    # ---------------------------------------------------------------------
    # Count of tickets (ticket_id)
    complaints_agg = complaints.groupby("customer_id").agg({
        "ticket_id": "count"
    }).reset_index()

    complaints_agg.rename(columns={
        "ticket_id": "complaint_count"
    }, inplace=True)

    master = master.merge(complaints_agg, on="customer_id", how="left")

    # ---------------------------------------------------------------------
    # 4. Call Center Logs Aggregation
    # ---------------------------------------------------------------------
    calls_agg = calls.groupby("customer_id").agg({
        "call_duration_min": "sum",
        "satisfaction_score": "mean",
    }).reset_index()

    calls_agg.rename(columns={
        "call_duration_min": "total_call_minutes",
        "satisfaction_score": "avg_call_satisfaction"
    }, inplace=True)

    master = master.merge(calls_agg, on="customer_id", how="left")

    # ---------------------------------------------------------------------
    # 5. Service History Aggregation
    # ---------------------------------------------------------------------
    service_agg = service.groupby("customer_id").agg({
        "service_type": "count",
        "amount_billed": "sum",
        "satisfaction_score": "mean"
    }).reset_index()

    service_agg.rename(columns={
        "service_type": "num_service_visits",
        "amount_billed": "total_service_billed",
        "satisfaction_score": "avg_service_satisfaction"
    }, inplace=True)

    master = master.merge(service_agg, on="customer_id", how="left")

    # ---------------------------------------------------------------------
    # 6. Sales Interactions Aggregation
    # ---------------------------------------------------------------------
    # Fields: salesperson, interaction_type, status
    sales_agg = sales.groupby("customer_id").agg({
        "interaction_type": "count",
        "status": lambda x: (x == "Completed").sum()
    }).reset_index()

    sales_agg.rename(columns={
        "interaction_type": "num_sales_interactions",
        "status": "successful_sales_interactions"
    }, inplace=True)

    master = master.merge(sales_agg, on="customer_id", how="left")

    # ---------------------------------------------------------------------
    # 7. Fill Missing Numerical Values
    # ---------------------------------------------------------------------
    master.fillna({
        "total_amount_paid": 0,
        "total_missed_payments": 0,
        "total_late_days": 0,
        "complaint_count": 0,
        "total_call_minutes": 0,
        "avg_call_satisfaction": 0,
        "num_service_visits": 0,
        "total_service_billed": 0,
        "avg_service_satisfaction": 0,
        "num_sales_interactions": 0,
        "successful_sales_interactions": 0
    }, inplace=True)

    return master
