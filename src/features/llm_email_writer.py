import os
from openai import OpenAI

client = OpenAI()


class LLMEmailWriter:
    """
    Persona-aware, tone-adjusting renewal email generator.
    Produces unique structure and messaging for each customer.
    """

    def __init__(self, model: str = "gpt-4.1-mini"):
        self.model = model

    # ---------------------------------------------------------
    # MAIN EMAIL WRITER
    # ---------------------------------------------------------
    def write_email(self, customer_info, reason, offer, language, tone):
        """
        customer_info includes:
            - customer_id
            - name
            - car_model
            - days_until_lease_end
            - churn_risk_bucket
            - churn_risk_score
            - nationality
            - persona_name
            - persona_emoji
            - persona_style (behavior description)
            - preferred_language
        """

        prompt = self._build_prompt(
            customer_info=customer_info,
            reason=reason,
            offer=offer,
            language=language,
            tone=tone,
        )

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system",
                 "content": "You are a highly skilled automotive retention strategist who writes human, persuasive, persona-tailored emails."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.65,  # <-- Higher temperature = more variation
        )

        return response.choices[0].message.content.strip()

    # ---------------------------------------------------------
    # PROMPT BUILDER
    # ---------------------------------------------------------
    def _build_prompt(self, customer_info, reason, offer, language, tone):
        """
        Builds a rich persona-aware prompt.
        """

        name = customer_info["name"]
        car = customer_info["car_model"]
        days = customer_info["days_until_lease_end"]
        churn = customer_info["churn_risk_bucket"]
        score = customer_info["churn_risk_score"]
        nationality = customer_info.get("nationality", "Unknown")

        persona_name = customer_info.get("persona_name", "General Customer")
        persona_emoji = customer_info.get("persona_emoji", "")
        persona_style = customer_info.get(
            "persona_style",
            "No behavior data available. Use a professional but warm style."
        )

        # -------------------------------
        # LANGUAGE LOGIC
        # -------------------------------
        if language == "ar":
            lang_instruction = "Write the entire email in professional Arabic."
        elif language == "en":
            lang_instruction = "Write the entire email in natural-sounding professional English."
        else:
            lang_instruction = (
                "If the customer nationality is from GCC, Egypt, Levant, Sudan, or Iraq, "
                "prefer Arabic. Otherwise use English. Ensure translation quality is flawless."
            )

        # -------------------------------
        # TONE STYLES (persona overrides may adjust this)
        # -------------------------------
        tone_map = {
            "direct": "concise, action-driven, and urgent",
            "warm": "friendly, emotional, and human",
            "warm_consultative": "empathetic, advisory, patient, and trust-building",
            "informative": "clear, factual, structured, and helpful",
            "reassuring": "supportive, calming, and positive",
            "neutral": "simple, polite, and professional",
        }

        tone_style = tone_map.get(tone, "professional and friendly")

        # -------------------------------
        # FINAL PROMPT
        # -------------------------------
        return f"""
Write a renewal email *fully tailored* to the customer's persona, culture, and situation.

### CUSTOMER PROFILE
- Name: {name}
- Nationality: {nationality}
- Car Model: {car}
- Days until lease end: {days}
- Churn Risk: {churn} (score {score:.2f})
- Reason for contact: {reason}

### PERSONA DETAILS
- Persona Type: {persona_name} {persona_emoji}
- Behavioral Traits: {persona_style}
- Adapt the writing style, tone, emotional intensity, structure, and negotiation strategy to this persona.

### OFFER TO INCLUDE
{offer}

### EMAIL REQUIREMENTS
1. Tone style to follow: **{tone_style}**
2. {lang_instruction}
3. Make the email STRUCTURE different depending on the persona:
   - High-Urgency personas → strong opening, bold CTA, short message
   - Analytical personas → structured bullets, logic, clarity
   - Price-sensitive personas → value justification, savings emphasis
   - Relationship personas → empathy, reassurance, human warmth
   - Busy Executive personas → extremely concise, no fluff
4. Reference the reason for contact naturally and in the persona’s preferred communication style.
5. Do NOT repeat the reason text word-for-word; reinterpret it.
6. Make the offer sound tailored — explain *why this customer* is receiving it.
7. Close with a CTA appropriate for the persona (assertive, soft, detailed, or minimal).
8. DO NOT invent financial details or numbers.

Write the email now.
"""
