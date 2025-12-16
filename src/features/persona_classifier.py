import numpy as np
"""
Persona Classifier
------------------
Rule-based persona assignment based on:
    • Nationality
    • Churn level
    • Complaints / service satisfaction
    • Total missed payments
    • Days until lease end

Returns:
    {
        "name": "High-Urgency Customer",
        "emoji": "🔥",
        "tone": "urgent_supportive",
        "language": "ar"  # or "en" or "auto"
    }
"""

class PersonaClassifier:

    def __init__(self):
        # Define persona mapping
        self.persona_definitions = {
            "High-Urgency Customer": {
                "emoji": "🔥",
                "tone": "urgent_supportive",
                "language": "auto",
            },
            "Luxury Calm Customer": {
                "emoji": "💎",
                "tone": "formal_luxury",
                "language": "en",
            },
            "Budget Value Customer": {
                "emoji": "💰",
                "tone": "friendly_reassuring",
                "language": "auto",
            },
            "Service-Sensitive Customer": {
                "emoji": "🛠️",
                "tone": "apologetic_recovery",
                "language": "auto",
            },
            "General Customer": {
                "emoji": "🙂",
                "tone": "warm_consultative",
                "language": "auto",
            },
        }

        # Nationalities commonly preferring Arabic
        self.arabic_nationalities = {
            "Egypt", "UAE", "Saudi Arabia", "Jordan", "Qatar",
            "Kuwait", "Bahrain", "Oman", "Lebanon"
        }

    # ----------------------------------------------------------------------
    # Helper: returns emoji from persona name
    # ----------------------------------------------------------------------
    def get_emoji_for_persona(self, persona_name):
        return self.persona_definitions.get(persona_name, {}).get("emoji", "🙂")

    # ----------------------------------------------------------------------
    # Core persona logic
    # ----------------------------------------------------------------------
    def predict_persona(self, row):
        """
        Takes a single customer record (row)
        Returns a persona profile dict:
            { name, emoji, tone, language }
        """

        nationality = row.get("nationality")
        complaints = row.get("complaint_count", 0)
        missed = row.get("total_missed_payments", 0)
        service_sat = row.get("avg_service_satisfaction", 5)
        churn = float(row.get("churn_risk_score", 0))
        days_left = int(row.get("days_until_lease_end", 90))
        segment = row.get("segment", "")

        # ---------------------------------------------------
        # 1. HIGH URGENCY: High churn + <15 days remaining
        # ---------------------------------------------------
        if churn >= 0.75 and days_left <= 15:
            persona_name = "High-Urgency Customer"

        # ---------------------------------------------------
        # 2. SERVICE SENSITIVE: Low satisfaction OR complaints
        # ---------------------------------------------------
        elif complaints > 0 or service_sat < 3:
            persona_name = "Service-Sensitive Customer"

        # ---------------------------------------------------
        # 3. LUXURY CALM CUSTOMER: Premium / luxury segments
        # ---------------------------------------------------
        elif segment in {"Luxury", "Premium"}:
            persona_name = "Luxury Calm Customer"

        # ---------------------------------------------------
        # 4. BUDGET VALUE CUSTOMER: Low payments & budget tier
        # ---------------------------------------------------
        elif segment in {"Mass Market", "Budget"} or row.get("monthly_payment", 0) < 1200:
            persona_name = "Budget Value Customer"

        # ---------------------------------------------------
        # 5. DEFAULT
        # ---------------------------------------------------
        else:
            persona_name = "General Customer"

        # ---------------------------------------------------
        # Language preference logic
        # ---------------------------------------------------
        preferred_language = "ar" if nationality in self.arabic_nationalities else "en"

        # ---------------------------------------------------
        # Return full persona structure
        # ---------------------------------------------------
        persona_profile = self.persona_definitions[persona_name].copy()

        persona_profile.update({
            "name": persona_name,
            "language": preferred_language  # override based on nationality
        })

        return persona_profile

