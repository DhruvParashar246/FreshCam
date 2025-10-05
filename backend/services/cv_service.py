from inference_sdk import InferenceHTTPClient
from dotenv import load_dotenv
from io import BytesIO
import os
import numpy as np
from PIL import Image

load_dotenv()

CLIENT = InferenceHTTPClient(
    api_url=os.getenv("https://detect.roboflow.com"),
    api_key=os.getenv("JrQNqqw3Sj1wzWj842i9"),
)

def analyze_image(image_bytes):
    image_stream = BytesIO(image_bytes)
    image = Image.open(image_stream).convert("RGB")

    image = image.resize((640, 640))

    result = CLIENT.infer(image, model_id="fruit-ripeness-unjex/2")

    preds = result.get("predictions", [])
    if not preds:
        return {"error": "No predictions found"}

    top_pred = max(preds, key=lambda x: x.get("confidence", 0))
    raw_class = top_pred.get("class", "unknown")
    stage = raw_class.split()[-1] if raw_class != "unknown" else "unknown"
    cleaned = {
        "ripeness": stage,
        "confidence": round(top_pred.get("confidence", 0) * 100, 2),
    }
    return cleaned

if __name__ == "__main__":
    with open("../images/ripe_mango.jpg", "rb") as image_file:
        image_bytes = image_file.read()
    output = analyze_image(image_bytes)
    print(output)