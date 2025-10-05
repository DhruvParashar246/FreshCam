import os
from typing import Optional, Tuple
import json

import google.generativeai as genai

_STORAGE_PROMPT = (
    "You are an expert food scientist. Provide a concise, practical storage plan for the given fruit to maximize freshness and longevity. "
    "Return only JSON with keys: {\n  \"advice\": \"<short paragraphs, plain text>\",\n  \"reason\": \"<one-line reason>\"\n}\n"
)


def _configure_genai():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name="gemini-1.5", generation_config={})


def generate_storage_advice(fruit: str, ripeness: Optional[str] = None, quantity: Optional[int] = None) -> Tuple[str, str]:
    """Return (advice_text, raw_text).

    In mock mode (GEMINI_API_KEY=mock) this returns canned advice.
    """
    if os.getenv("GEMINI_API_KEY") == "mock":
        f = fruit.lower()
        # Simple canned responses
        canned = {
            "apple": {
                "advice": "Store apples in the refrigerator crisper drawer in a breathable bag; keep away from strong-smelling foods. Separate any bruised apples.",
                "reason": "Cool, humid conditions slow respiration and microbial growth."
            },
            "banana": {
                "advice": "Keep bananas at room temperature away from direct sunlight; refrigerate only after ripening to extend 2-3 days (peel may darken).",
                "reason": "Bananas are tropical and susceptible to chill injury; refrigeration slows ripening but changes peel color."
            },
            "strawberry": {
                "advice": "Refrigerate strawberries unwashed in a shallow container lined with paper towel and loosely covered. Use within a few days.",
                "reason": "High water content and delicate skin cause rapid spoilage."
            },
        }
        pick = canned.get(f, {"advice": f"Store {fruit} in a cool, dry place or refrigerate depending on type.", "reason": "General guidance"})
        raw = json.dumps({"advice": pick["advice"], "reason": pick["reason"]})
        return pick["advice"], raw

    model = _configure_genai()
    # Build a targeted prompt
    details = f"Fruit: {fruit}."
    if ripeness:
        details += f" Ripeness: {ripeness}."
    if quantity:
        details += f" Quantity: {quantity}."

    prompt = _STORAGE_PROMPT + "\nDetails:\n" + details

    resp = model.generate_text(prompt)
    raw = (resp.text or "").strip()

    # Try to parse JSON
    try:
        parsed = json.loads(raw)
        advice = parsed.get("advice") or json.dumps(parsed)
        return advice, raw
    except Exception:
        # If not JSON, return the raw text as advice
        return raw, raw
