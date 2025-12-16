import streamlit as st
import pandas as pd
import os

from src.agent.engine import CustomerAgent

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="High-Risk Customer Dashboard — AI Assistant",
    layout="wide"
)

st.title("🚨 High-Risk Customer Dashboard — AI Assistant")
st.caption(
    "Grid view of high-risk customers + on-demand email generation + approve/reject workflow."
)

# --------------------------------------------------
# Session state
# --------------------------------------------------
if "selected_customer_id" not in st.session_state:
    st.session_state.selected_customer_id = None

if "generated_packet" not in st.session_state:
    st.session_state.generated_packet = None

# --------------------------------------------------
# Load dataset
# --------------------------------------------------
@st.cache_data(show_spinner=True)
def load_featured():
    file_path = "master_featured.csv"

    if not os.path.exists(file_path):
        st.error(f"Dataset not found: {file_path}")
        st.stop()

    df = pd.read_csv(file_path)
    return df, file_path


df, used_path = load_featured()

st.info(f"📄 Loaded dataset from: `{os.path.abspath(used_path)}` | Rows: {len(df):,}")

# --------------------------------------------------
# Filter high-risk customers ONLY
# --------------------------------------------------
high_risk_df = df[df["churn_risk_bucket"] == "High"].copy()

if high_risk_df.empty:
    st.error("No high-risk customers found.")
    st.stop()

# --------------------------------------------------
# Agent
# --------------------------------------------------
agent = CustomerAgent(high_risk_df)

# --------------------------------------------------
# Top 10 highest churn probability
# --------------------------------------------------
st.subheader("🏁 Top 10 highest churn probability")

top10 = (
    high_risk_df
    .sort_values("churn_prob", ascending=False)
    .head(10)[
        [
            "customer_id",
            "name",
            "car_model",
            "nationality",
            "churn_prob",
            "days_until_lease_end",
        ]
    ]
)

st.dataframe(top10, use_container_width=True)

# --------------------------------------------------
# All high-risk customers (grid with buttons)
# --------------------------------------------------
st.subheader("📋 All high-risk customers (grid)")

for _, row in high_risk_df.iterrows():
    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])

    c1.write(row["customer_id"])
    c2.write(row["name"])
    c3.write(row["car_model"])
    c4.write(f"{row['churn_prob']:.2f}")

    if c5.button("✉️ Generate Email", key=row["customer_id"]):
        st.session_state.selected_customer_id = row["customer_id"]
        st.session_state.generated_packet = None

# --------------------------------------------------
# Email workflow (only after clicking a row)
# --------------------------------------------------
if st.session_state.selected_customer_id:
    st.divider()
    st.subheader("📄 Customer details + email workflow")

    selected_row = high_risk_df[
        high_risk_df["customer_id"] == st.session_state.selected_customer_id
    ].iloc[0]

    left, right = st.columns([1, 1.3])

    # ---------------- LEFT: profile & risk ----------------
    with left:
        st.subheader("👤 Profile")

        st.write(f"**Name:** {selected_row['name']}")
        st.write(f"**Customer ID:** `{selected_row['customer_id']}`")
        st.write(f"**Car Model:** {selected_row['car_model']}")
        st.write(f"**Nationality:** {selected_row.get('nationality', 'N/A')}")
        st.write(f"**Segment:** {selected_row.get('segment', 'N/A')}")

        st.markdown("---")
        st.subheader("⚠️ Risk Summary")

        st.write(f"**Churn Probability:** {selected_row['churn_prob']:.2f}")
        st.write(f"**Days until lease end:** {selected_row['days_until_lease_end']}")

        reasons = agent._build_reason_text(selected_row)
        st.write(f"**Risk factors:** {reasons}")

        st.markdown("---")
        st.subheader("🔎 Raw drivers")
        st.write(f"• Missed payments: {selected_row.get('total_missed_payments', 0)}")
        st.write(f"• Complaints: {selected_row.get('complaint_count', 0)}")
        st.write(f"• Avg service satisfaction: {selected_row.get('avg_service_satisfaction', 'N/A')}")

    # ---------------- RIGHT: email ----------------
    with right:
        st.subheader("✉️ AI Email Draft")

        if st.button("🧠 Generate / Regenerate Email"):
            packet = agent.build_action_packet(selected_row)
            st.session_state.generated_packet = packet

        if st.session_state.generated_packet:
            packet = st.session_state.generated_packet

            email_text = st.text_area(
                "Email body (editable):",
                value=packet["email_to_sales"],
                height=320
            )

            feedback = st.text_area("Feedback (optional):")

            col_a, col_b = st.columns(2)

            if col_a.button("✅ Approve (Demo: Gmail disabled)"):
                st.success("Approved. (In demo mode, Gmail is not triggered.)")

            if col_b.button("❌ Reject + Save Feedback"):
                st.info("Rejected. Feedback saved for learning loop.")
