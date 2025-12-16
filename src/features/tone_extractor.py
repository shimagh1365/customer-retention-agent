from openai import OpenAI
client = OpenAI()

def extract_tone_signals(call_transcript: str) -> dict:
    prompt = f"""
Analyze the following customer call and extract communication behavior patterns.

CALL TRANSCRIPT:
--------------------------------
{call_transcript}
--------------------------------

Return a JSON with:
- preferred_language: "en" or "ar"
- preferred_tone: one of:
    "warm_consultative", "premium_concise",
    "apologetic_recovery", "direct_transactional"
- frustration_level: "low", "medium", "high"
- price_sensitivity: "low", "medium", "high"
- emotional_style: description in 1 sentence
- closure_preference: "direct", "soft", "detailed"
- notes: short plain text summary
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return response.choices[0].message.content
