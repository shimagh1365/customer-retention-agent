Customer Retention AI Agent (Demo Version)

This repository contains a Customer Retention AI Agent designed to help sales teams identify high-risk customers, understand why they are at risk, and proactively generate renewal outreach using AI — with full human approval.

What this system does

Analyzes customer, lease, payment, service, and interaction data

Scores customers by churn risk

Displays high-risk customers in a grid for easy review

Explains why each customer is flagged (missed payments, low satisfaction, lease expiry, etc.)

Generates AI-written renewal emails tailored to customer behavior and persona

Allows sales users to approve, reject, or give feedback before sending

Learns preferred tone over time via a lightweight customer memory layer

What this system does NOT do

❌ Does not send emails automatically without human approval

❌ Does not expose or export customer data outside internal systems

❌ Does not replace sales decision-making

Architecture (High-level)

Data Layer: CRM, DMS, Leasing, Aftersales, Call Center (or synthetic equivalents)

AI Agent Core: Risk scoring, persona logic, LLM email generation

Human-in-the-Loop UI: Streamlit dashboard for review and action

Output: Draft emails prepared for salesperson approval

Purpose of this repository

This project is intended as:

A proof-of-concept / demo

A foundation for production development

A safe, explainable AI assistant for customer retention workflows

All datasets used in this repository are synthetic.
No real customer data, credentials, or emails are stored.
