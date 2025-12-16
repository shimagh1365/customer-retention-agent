import pandas as pd

from src.agent.llm_email_writer import LLMEmailWriter
from src.features.persona import choose_tone_when_no_data
from src.memory.customer_memory_db import CustomerMemoryDB
from src.features.persona_classifier import PersonaClassifier


class CustomerAgent:
    """
    SAFE demo-ready agent.

    Gmail is NOT initialized unless explicitly requested.
    """

    def __init__(self, featured_df: pd.DataFrame):
        self.df = featured_df

        self.llm = LLMEmailWriter()
        self.memory = CustomerMemoryDB()
        self.personas = PersonaClassifier()

        # Gmail is optional — DO NOT init here
        self.gmail = None

    # ------------------------------------------------------------------
    # INTERNAL: build reason text
    # ------------------------------------------------------------------
    def _build_reason_text(self, row):
        reasons = []

        if row.get("total_missed_payments", 0) > 0:
            reasons.append("Past missed payments")

        if row.get("complaint_count", 0) > 0:
            reasons.append("Recent complaints")

        if row.get("avg_service_satisfaction", 5) < 3:
            reasons.append("Low service satisfaction")

        if row.get("days_until_lease_end", 999) <= 30:
            reasons.append("Lease ending soon")

        if row.get("churn_risk_bucket") == "High":
            reasons.append("High churn risk")

        return ", ".join(reasons) if reasons else "General follow-up"

    # ------------------------------------------------------------------
    # OFFER ENGINE
    # ------------------------------------------------------------------
    def suggest_offer(self, row):
        days = row.get("days_until_lease_end", 90)
        missed = row.get("total_missed_payments", 0)
        satisfaction = row.get("avg_service_satisfaction", 5)

        if missed > 0:
            return "10% renewal discount + free service"
        if satisfaction < 3:
            return "Complimentary full service"
        if days <= 10:
            return "Free tire replacement voucher"

        return "Personalized renewal consultation call"

    # ------------------------------------------------------------------
    # PERSONA + TONE
    # ------------------------------------------------------------------
    def _determine_tone_and_language(self, row):
        mem = self.memory.load_tone(row["customer_id"])
        if mem:
            return (
                mem.get("preferred_tone", "warm_consultative"),
                mem.get("preferred_language", "auto"),
                mem.get("persona_name", "General Customer"),
            )

        persona = self.personas.predict_persona(row)

        return (
            persona.get("tone", "warm_consultative"),
            persona.get("language", "auto"),
            persona.get("name", "General Customer"),
        )

    # ------------------------------------------------------------------
    # EMAIL GENERATION
    # ------------------------------------------------------------------
    def generate_sales_email(self, row, reason_text):
        offer = self.suggest_offer(row)
        tone, language, persona_name = self._determine_tone_and_language(row)

        customer_info = {
            "customer_id": row["customer_id"],
            "name": row["name"],
            "car_model": row["car_model"],
            "days_until_lease_end": int(row.get("days_until_lease_end", 0)),
            "churn_risk_bucket": row.get("churn_risk_bucket"),
            "churn_risk_score": float(row.get("churn_prob", 0)),
            "nationality": row.get("nationality"),
            "persona_name": persona_name,
            "preferred_language": language,
        }

        email_text = self.llm.write_email(
            customer_info=customer_info,
            reason=reason_text,
            offer=offer,
            language=language,
            tone=tone,
        )

        return email_text, tone, language, persona_name

    # ------------------------------------------------------------------
    # ACTION PACKET (UI-safe)
    # ------------------------------------------------------------------
    def build_action_packet(self, row):
        reason_text = self._build_reason_text(row)
        email_text, tone, lang, persona_name = self.generate_sales_email(row, reason_text)

        persona_emoji_map = {
            "High-Urgency Customer": "🔥",
            "Price-Sensitive Customer": "💰",
            "VIP Loyalist": "⭐",
            "Silent At-Risk": "⚠️",
            "General Customer": "🙂",
        }

        offer = self.suggest_offer(row)
        offer_emoji_map = {
            "10% renewal discount + free service": "💸",
            "Free tire replacement voucher": "🛞",
            "Complimentary full service": "🛠️",
            "Personalized renewal consultation call": "📞",
        }

        return {
            "customer_id": row["customer_id"],
            "name": row["name"],
            "car_model": row["car_model"],
            "nationality": row.get("nationality"),
            "churn_risk_bucket": row.get("churn_risk_bucket"),
            "churn_risk_score": float(row.get("churn_prob", 0)),
            "days_until_lease_end": int(row.get("days_until_lease_end", 0)),
            "persona_name": persona_name,
            "persona_emoji": persona_emoji_map.get(persona_name, "🙂"),
            "reason": reason_text,
            "recommended_offer": offer,
            "offer_emoji": offer_emoji_map.get(offer, "🎁"),
            "email_to_sales": email_text,
            "used_tone": tone,
            "used_language": lang,
            "status": "DRAFT_CREATED",
        }

    # ------------------------------------------------------------------
    # HIGH-RISK ONLY (GRID SAFE)
    # ------------------------------------------------------------------
    def create_sales_draft_packets(self):
        high_risk_df = self.df[self.df["churn_risk_bucket"] == "High"]

        return [
            self.build_action_packet(row)
            for _, row in high_risk_df.iterrows()
        ]

    # ------------------------------------------------------------------
    # OPTIONAL: Gmail send (ONLY when button clicked)
    # ------------------------------------------------------------------
    def send_email_draft_to_sales(self, packet, salesperson_email, sender_email):
        from src.email.gmail_sender import GmailDraftSender

        if self.gmail is None:
            self.gmail = GmailDraftSender()

        subject = f"Draft: {packet['name']} ({packet['customer_id']}) – Renewal"

        return self.gmail.create_draft(
            sender_email=sender_email,
            to_email=salesperson_email,
            subject=subject,
            body_text=packet["email_to_sales"],
        )
