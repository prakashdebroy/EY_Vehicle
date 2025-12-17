import os
import google.generativeai as genai
import dotenv

dotenv.load_dotenv()

SYSTEM_PROMPT = """You are the voice of a car. Style: calm, concise, non-technical unless urgent.
Given SENSOR JSON and ALERTS, produce ONE short spoken sentence (max ~18 words).
Prefer actionable advice. If critical, start with 'Attention'.
Do not repeat raw numbers unless necessary. No emojis.
"""

def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def craft_line(model, sensors: dict, alerts: list) -> str:
    alerts_compact = [{"level": a.level, "code": a.code} for a in alerts]
    user_payload = {
        "sensors": sensors,
        "alerts": alerts_compact
    }
    prompt = f"{SYSTEM_PROMPT}\nSENSOR={user_payload}"
    resp = model.generate_content(prompt)
    text = (resp.text or "").strip()
    # fallback if model returns empty
    if not text:
        if alerts:
            text = "Attention: check the highlighted warnings."
        else:
            text = "All systems normal."
    return text
