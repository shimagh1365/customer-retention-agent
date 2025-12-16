"""
Persona → tone/language mapping module.

Used when:
    • persona_classifier gives us a persona_key
    • memory DB does not contain a learned tone yet
    • zero-data fallback still needed

This module keeps all persona–tone–language relationships
clean, centralized and easy to update.
"""

# ----------------------------
# PERSONA → TONE PRESETS
# ----------------------------

PERSONA_TONE_MAP = {
    "high_urgency": "urgent_supportive",      # 🔥
    "service_sensitive": "warm_apologetic",   # 🛠️
    "price_sensitive": "value_reinforcing",   # 💸
    "general": "friendly_professional",       # 🙂
}

# ----------------------------
# PERSONA → LANGUAGE PRESETS
# ----------------------------
def preferred_language_from_nationality(nationality):
    """
    Arabic-first logic for fallback.
    """

    if not nationality:
        return "en"

    nat = nationality.lower()

    arabic_group = {
        "uae", "united arab emirates", "emirati",
        "ksa", "saudi", "saudi arabia",
        "jordan", "egypt", "oman", "kuwait",
        "qatar", "bahrain"
    }

    if nat in arabic_group:
        return "ar"

    return "en"

# ----------------------------
# FALLBACK TONE WHEN NOTHING EXISTS
# ----------------------------
def choose_tone_when_no_data(segment=None, nationality=None):
    """
    Simple deterministic fallback used if:
        • persona_classifier failed
        • customer_memory has no entry
    """

    seg = (segment or "").lower()

    # Language
    language = preferred_language_from_nationality(nationality)

    # Tone based on segment
    if seg in ["premium", "luxury"]:
        tone = "warm_consultative"
    elif seg in ["mass market", "retail"]:
        tone = "value_reinforcing"
    else:
        tone = "friendly_professional"

    return tone

# ----------------------------
# GET TONE FROM PERSONA
# ----------------------------
def tone_from_persona(persona_key):
    """
    Given "price_sensitive" → "value_reinforcing"
    """
    return PERSONA_TONE_MAP.get(persona_key, "friendly_professional")


# ----------------------------
# DESCRIPTIVE LABELS FOR UI
# ----------------------------
PERSONA_DESCRIPTION = {
    "high_urgency": "Needs immediate attention — likely to churn soon. Respond quickly with supportive tone.",
    "service_sensitive": "Cares about service quality. Use empathetic tone and highlight resolution steps.",
    "price_sensitive": "Focused on costs and value. Emphasize discounts, savings, and offer clarity.",
    "general": "Standard customer, neutral expectations. Use friendly, professional tone.",
}

def persona_description(persona_key):
    return PERSONA_DESCRIPTION.get(persona_key, "General customer")
