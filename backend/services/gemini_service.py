import os
import json
from typing import List, Dict, Any, Tuple

import google.generativeai as genai

_ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"}

_PROMPT = """You are a strict fruit identifier.

Return ONLY compact JSON matching this schema (no prose, no markdown fences):
{
  "fruit": "<lowercase canonical fruit name or 'unknown'>",
  "confidence": <float between 0 and 1>,
  "alternatives": [{"fruit": "<name>", "confidence": <0..1>}, ... up to 3],
  "reason": "<very short reason>"
}

Rules:
- If not a single clear fruit, return fruit="unknown", confidence<=0.2, and a short reason.
- Use common names (banana, apple, mango, avocado, strawberry, blueberry, orange, lemon, lime, peach, pear, plum, pineapple, watermelon, cantaloupe, honeydew, grape, tomato).
- Be conservative; don't overclaim.
"""

def _configure():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")
    genai.configure(api_key=api_key)
    # You can swap models; 1.5 Flash is fast and good for vision
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            # Strongly nudge JSON output:
            "response_mime_type": "application/json",
        },
    )

def _image_part(image_bytes: bytes, mime_type: str) -> Dict[str, Any]:
    mt = (mime_type or "").lower()
    if mt not in _ALLOWED_MIME:
        # fall back if unknown; JPEG works widely
        mt = "image/jpeg"
    return {"mime_type": mt, "data": image_bytes}

def identify_fruit(image_bytes: bytes, mime_type: str) -> Tuple[Dict[str, Any], str]:
    """
    Calls Gemini on a single image and returns (parsed_json, raw_text).
    parsed_json has keys: fruit, confidence, alternatives, reason
    """
    model = _configure()
    parts = [_image_part(image_bytes, mime_type), _PROMPT]

    resp = model.generate_content(parts)
    # Some SDK versions return .text, some .candidates[0].content.parts[0].text; .text is unified
    raw = (resp.text or "").strip()

    # Try strict json parsing; if it fails, attempt to strip code fences
    try:
        return json.loads(raw), raw
    except Exception:
        # Try to extract the first {...} block
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw[start : end + 1]), raw
            except Exception:
                pass
        # Last resort—return a conservative unknown
        return {
            "fruit": "unknown",
            "confidence": 0.0,
            "alternatives": [],
            "reason": "Could not parse Gemini response"
        }, raw


def identify_fruit_from_file(image_path: str, debug: bool = False) -> Tuple[Dict[str, Any], str]:
    """
    Convenience helper to identify a fruit from an image file path.

    This function supports a local mock mode for development: set the environment
    variable GEMINI_API_KEY to the literal value "mock" to enable filename-based
    identification (no network calls). Otherwise it will read the file bytes and
    call `identify_fruit` which invokes Gemini.

    Returns (parsed_json, raw_text)
    """
    # Simple extension -> mime mapping
    ext = os.path.splitext(image_path)[1].lower()
    mime = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".heic": "image/heic",
        ".heif": "image/heif",
    }.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        data = f.read()

    # Mock mode: map known filenames to fruits for local testing without Gemini
    # Enable by setting: export GEMINI_API_KEY=mock
    if os.getenv("GEMINI_API_KEY") == "mock":
        name = os.path.basename(image_path).lower()
        mapping = {
            "ripe_apple": ("apple", 0.95),
            "unripe_apple": ("apple", 0.25),
            "ripe_banana": ("banana", 0.95),
            "unripe_banana": ("banana", 0.15),
            "ripe_mango": ("mango", 0.95),
            "ripe_strawberry": ("strawberry", 0.95),
        }
        chosen = ("unknown", 0.0)
        for k, v in mapping.items():
            if k in name:
            if os.getenv("GEMINI_API_KEY") == "mock":
                break

        fruit, confidence = chosen
        parsed = {
            "fruit": fruit,
            "confidence": float(confidence),
            "alternatives": [],
            "reason": "mocked by filename",
        }
        raw = json.dumps(parsed)
        return parsed, raw

    # Normal mode: forward bytes to Gemini integration
    return identify_fruit(data, mime)
