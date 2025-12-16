import os
from openai import OpenAI

client = OpenAI()


class LLMEmailWriter:
    """
    Generates tone-aware, persona-aware email drafts for salespeople.
    """

    def __init__(self, model: str = "gpt-4.1-mini"):
        self.model = model

    # ---------------------------------------------------------
    # Main Email Writer
    # ---------------------------------------------------------
    def write_email(self, customer_info, reason, offer, language, tone):
        """
        customer_info: dict containing key customer attributes
        reason: AI reason for contacting the customer
        offer: AI-selected offer
        """

        # Build “offer explanation” for the LLM
        offer_explanation = self._explain_offer(reason, offer)

        prompt = self._build_prompt(
            customer_info=customer_info,
            reason=reason,
            offer=offer,
            language=language,
            tone=tone,
            offer_explanation=offer_explanation
        )

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system",
                 "content": "You are a professional automotive retention email writer who explains offers clearly and tactfully."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    # ---------------------------------------------------------
    # OFFER EXPLANATION
    # ---------------------------------------------------------
    def _explain_offer(self, reason, offer):
        """
        Converts the reason + offer into a clear internal explanation
        that the LLM should use when writing the email.
        """

        reason_lower = reason.lower()

        # Map offer types to general explanations
        if "discount" in offer.lower():
            if "10%" in offer or "15%" in offer:
                return (
                    "Because the customer is at high churn risk or their lease is ending soon, "
                    "a renewal discount helps reduce financial friction and encourages them "
                    "to stay with the dealership."
                )

        if "free service" in offer.lower():
            return (
                "The customer has a history of complaints or missed payments, so offering a free "
                "service builds trust, reduces stress, and shows commitment to supporting them."
            )

        if "tire" in offer.lower() or "inspection" in offer.lower():
            return (
                "The customer has a high number of service visits, indicating that maintenance support "
                "is valuable to them. Offering free tires or an inspection reinforces reliability."
            )

        if "detailing" in offer.lower():
            return (
                "The customer has multiple complaints, so a premium service gesture like detailing "
                "helps restore satisfaction and shows appreciation."
            )

        if "loyalty" in offer.lower():
            return (
                "The customer belongs to a valuable loyalty tier, so rewarding them strengthens "
                "long-term retention and customer lifetime value."
            )

        return (
            "The offer is tailored to the customer’s profile to increase renewal likelihood while "
            "addressing their needs and improving satisfaction."
        )

    # ---------------------------------------------------------
    # Prompt Builder
    # ---------------------------------------------------------
    def _build_prompt(self, customer_info, reason, offer, language, tone, offer_explanation):
        """
        Converts customer + persona context into an instruction suitable for the LLM.
        """

        name = customer_info["name"]
        car = customer_info["car_model"]
        days = customer_info["days_until_lease_end"]
        churn = customer_info["churn_risk_bucket"]
        score = customer_info["churn_risk_score"]

        # Language rules
        if language == "ar":
            lang_instruction = "Write the entire email in professional Arabic."
        elif language == "en":
            lang_instruction = "Write the entire email in professional English."
        else:
            lang_instruction = (
                "If the customer's nationality is from GCC (UAE, KSA, Oman, Qatar, Bahrain, Kuwait, Jordan, Egypt), "
                "prefer Arabic. Otherwise write in professional English."
            )

        # Tone styles
        tone_map = {
            "direct": "short, clear, and urgency-focused",
            "warm": "friendly, reassuring, and human",
            "warm_consultative": "empathetic, advisory, and relationship-focused",
            "informative": "clear, factual, benefit-driven",
            "reassuring": "soft, supportive, calming, trust-building",
            "neutral": "professional, simple, polite"
        }

        tone_style = tone_map.get(tone, "professional and friendly")

        return f"""
You are writing a renewal email from an automotive sales team to a customer.

### CUSTOMER DETAILS
- Name: {name}
- Car Model: {car}
- Days until lease end: {days}
- Churn risk: {churn} (score {score:.2f})

### REASON FOR CONTACT
{reason}

### OFFER SELECTED
{offer}

### WHY THIS OFFER (EXPLANATION FOR YOU TO USE)
{offer_explanation}
Explain the offer benefits naturally in the email without sounding robotic.
Do NOT mention that this reasoning comes from the system.

### INSTRUCTIONS
- Tone style: {tone_style}
- {lang_instruction}
- Highlight why the offer is valuable *based directly on the customer situation*.
- Do NOT add fake financial numbers or unrealistic claims.
- Keep the email concise, warm, and aligned with the persona.
- End with a friendly invitation to contact the salesperson.

Write the full email now.
"""
