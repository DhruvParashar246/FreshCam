import json
import os
import re
from io import BytesIO

import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model with vision capabilities - using Gemini 2.0 Flash
# Configure safety settings to be more permissive for food images
from google.generativeai.types import HarmBlockThreshold, HarmCategory

safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

model = genai.GenerativeModel("gemini-2.0-flash-exp", safety_settings=safety_settings)


def get_fruit_name(image_bytes):
    """
    Get the name of the fruit from the image using Gemini Vision API.

    Args:
        image_bytes: Raw image bytes

    Returns:
        dict: {"fruit_name": "apple"} or {"error": "..."}
    """
    try:
        print("🍎 Getting fruit name from Gemini...")
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        prompt = """Identify the fruit in this image. Return ONLY the fruit name in lowercase, nothing else.
Examples: apple, banana, mango, strawberry, orange, etc.
If you cannot identify a fruit, return 'unknown'."""

        response = model.generate_content([prompt, image])

        print(
            f"Fruit name response: {response.text if hasattr(response, 'text') else 'No text'}"
        )

        if not response or not hasattr(response, "text") or not response.text:
            print("❌ No fruit name response from Gemini")
            return {"fruit_name": "unknown"}

        # Clean up the response - remove extra whitespace and convert to lowercase
        fruit_name = response.text.strip().lower()

        # Remove any punctuation or extra words - just get the fruit name
        fruit_name = re.sub(r"[^a-z\s]", "", fruit_name)
        fruit_name = fruit_name.split()[0] if fruit_name.split() else "unknown"

        print(f"✓ Fruit identified: {fruit_name}")
        return {"fruit_name": fruit_name}

    except Exception as e:
        print(f"❌ Error in get_fruit_name: {e}")
        import traceback

        traceback.print_exc()
        return {"fruit_name": "unknown"}


def analyze_ripeness_with_gemini(image_bytes):
    """
    Analyze fruit ripeness using Gemini Vision API as a fallback.

    Args:
        image_bytes: Raw image bytes

    Returns:
        dict: {"fruit_name": "apple", "ripeness": "ripe", "confidence": 85.0}
              or {"error": "..."}
    """
    try:
        print("🔍 Starting Gemini ripeness analysis...")
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        print(f"✓ Image loaded: {image.size}")

        prompt = """Analyze this fruit image and determine:
1. The fruit name (e.g., apple, banana, mango, strawberry)
2. Its ripeness stage: must be one of these exact values: "unripe", "ripe", or "overripe"

Criteria:
- unripe: green, hard, not ready to eat
- ripe: perfect for eating, good color, firm
- overripe: brown spots, very soft, past prime

Respond in EXACTLY this JSON format with no additional text:
{
  "fruit_name": "name of fruit in lowercase",
  "ripeness": "unripe/ripe/overripe",
  "confidence": 85.0
}"""

        print("📤 Sending to Gemini API...")
        response = model.generate_content([prompt, image])

        print(f"📥 Response received: {response}")

        # Check if response was blocked
        if hasattr(response, "prompt_feedback"):
            print(f"Prompt feedback: {response.prompt_feedback}")

        if not response or not hasattr(response, "text") or not response.text:
            print("❌ No text in response")
            return {"error": "No response from Gemini"}

        # Try to parse JSON from response
        text = response.text.strip()
        print(f"📝 Response text: {text}")

        # Remove markdown code blocks if present
        text = re.sub(r"```json\s*", "", text)
        text = re.sub(r"```\s*", "", text)

        try:
            result = json.loads(text)
            print(f"✓ JSON parsed successfully: {result}")

            # Validate and clean the response
            fruit_name = result.get("fruit_name", "unknown").lower()
            ripeness = result.get("ripeness", "unknown").lower()
            confidence = float(result.get("confidence", 75.0))

            # Ensure ripeness is one of the valid values
            if ripeness not in ["unripe", "ripe", "overripe"]:
                ripeness = "ripe"  # Default to ripe if unclear

            final_result = {
                "fruit_name": fruit_name,
                "ripeness": ripeness,
                "confidence": round(confidence, 2),
                "source": "gemini",
            }
            print(f"✅ Final result: {final_result}")
            return final_result

        except json.JSONDecodeError as je:
            print(f"⚠️ JSON decode failed: {je}")
            # If JSON parsing fails, try to extract info manually
            text_lower = text.lower()

            # Extract ripeness
            ripeness = "unknown"
            if "unripe" in text_lower:
                ripeness = "unripe"
            elif "overripe" in text_lower:
                ripeness = "overripe"
            elif "ripe" in text_lower:
                ripeness = "ripe"

            # Try to extract fruit name
            fruit_name = "unknown"
            common_fruits = [
                "apple",
                "banana",
                "mango",
                "strawberry",
                "orange",
                "grape",
                "pear",
                "peach",
                "plum",
                "cherry",
            ]
            for fruit in common_fruits:
                if fruit in text_lower:
                    fruit_name = fruit
                    break

            return {
                "fruit_name": fruit_name,
                "ripeness": ripeness,
                "confidence": 70.0,
                "source": "gemini",
            }

    except Exception as e:
        print(f"❌ Error in analyze_ripeness_with_gemini: {e}")
        return {"error": str(e)}


def get_recipes_and_safety(image_bytes, fruit_name=None, ripeness=None):
    """
    Get recipe suggestions, food safety information, and estimated shelf life
    based on fruit image and ripeness level.

    Args:
        image_bytes: Raw image bytes
        fruit_name: Optional fruit name (if already detected)
        ripeness: Optional ripeness level (if already detected)

    Returns:
        dict: {
            "fruit_name": "banana",
            "ripeness": "ripe",
            "is_safe_to_eat": true,
            "days_until_discard": 3,
            "storage_tips": "...",
            "recipes": [
                {
                    "name": "Banana Smoothie",
                    "difficulty": "easy",
                    "prep_time": "5 minutes",
                    "ingredients": [...],
                    "instructions": "..."
                }
            ]
        }
    """
    try:
        print("🍳 Getting recipes and safety info from Gemini...")
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        # Build context from provided info
        context = ""
        if fruit_name and ripeness:
            context = f"\nThe fruit has been identified as: {fruit_name}\nCurrent ripeness: {ripeness}"

        prompt = f"""Analyze this fruit image and provide comprehensive information to reduce food waste.{context}

Please provide:
1. **Fruit identification** (if not already provided)
2. **Ripeness level**: unripe, ripe, or overripe
3. **Food safety**: Is it safe to eat? (yes/no)
4. **Estimated days**: How many days until it should be discarded? (0-14 days)
5. **Storage tips**: Best way to store to maximize freshness
6. **Recipe suggestions**: 3 recipes optimized for this ripeness level to minimize waste

Criteria:
- **Unripe fruits**: Recipes that work with firm, tart fruits OR how to ripen them
- **Ripe fruits**: Best-use recipes for peak freshness
- **Overripe fruits**: Recipes that utilize very soft/spotted fruits (smoothies, baking, etc.)

Respond in EXACTLY this JSON format:
{{
  "fruit_name": "banana",
  "ripeness": "overripe",
  "is_safe_to_eat": true,
  "days_until_discard": 2,
  "storage_tips": "Store overripe bananas in the freezer for smoothies or baking. They can last months frozen.",
  "recipes": [
    {{
      "name": "Banana Bread",
      "difficulty": "easy",
      "prep_time": "15 minutes",
      "cook_time": "60 minutes",
      "why_this_ripeness": "Overripe bananas are perfect for banana bread - they're sweeter and mash easily",
      "ingredients": [
        "3 overripe bananas, mashed",
        "1/3 cup melted butter",
        "1 cup sugar",
        "1 egg, beaten",
        "1 tsp vanilla",
        "1 tsp baking soda",
        "Pinch of salt",
        "1.5 cups flour"
      ],
      "instructions": "1. Preheat oven to 350°F. 2. Mix butter and mashed bananas. 3. Add sugar, egg, and vanilla. 4. Mix in baking soda and salt. 5. Add flour, mix until just combined. 6. Pour into greased loaf pan. 7. Bake 60 minutes until golden."
    }},
    {{
      "name": "Banana Smoothie",
      "difficulty": "very easy",
      "prep_time": "3 minutes",
      "cook_time": "0 minutes",
      "why_this_ripeness": "Very ripe bananas add natural sweetness and creamy texture",
      "ingredients": [
        "2 overripe bananas",
        "1 cup milk or almond milk",
        "1/2 cup yogurt",
        "1 tbsp honey (optional)",
        "Ice cubes"
      ],
      "instructions": "1. Peel bananas and break into chunks. 2. Add all ingredients to blender. 3. Blend until smooth. 4. Serve immediately."
    }},
    {{
      "name": "Frozen Banana Bites",
      "difficulty": "very easy",
      "prep_time": "10 minutes",
      "cook_time": "0 minutes (2 hours freezing)",
      "why_this_ripeness": "Saves overripe bananas from waste and makes a healthy treat",
      "ingredients": [
        "2-3 overripe bananas",
        "Melted chocolate or peanut butter",
        "Optional toppings: nuts, coconut, sprinkles"
      ],
      "instructions": "1. Slice bananas into rounds. 2. Dip in melted chocolate or spread with peanut butter. 3. Add toppings. 4. Freeze on parchment paper for 2 hours. 5. Store in freezer bag."
    }}
  ]
}}

Important: 
- Be realistic about food safety - if moldy or rotten, mark as unsafe
- Days until discard should be conservative and safe
- Recipes must be practical and use the fruit at its current ripeness"""

        print("📤 Sending recipe request to Gemini...")
        response = model.generate_content([prompt, image])

        if hasattr(response, "prompt_feedback"):
            print(f"Prompt feedback: {response.prompt_feedback}")

        if not response or not hasattr(response, "text") or not response.text:
            print("❌ No response from Gemini for recipes")
            return {"error": "No response from Gemini"}

        text = response.text.strip()
        print(f"📝 Recipe response length: {len(text)} chars")

        # Remove markdown code blocks if present
        text = re.sub(r"```json\s*", "", text)
        text = re.sub(r"```\s*", "", text)

        try:
            result = json.loads(text)
            print(f"✅ Recipe data parsed successfully")
            print(f"   - Fruit: {result.get('fruit_name')}")
            print(f"   - Safe to eat: {result.get('is_safe_to_eat')}")
            print(f"   - Days remaining: {result.get('days_until_discard')}")
            print(f"   - Recipes: {len(result.get('recipes', []))}")

            return result

        except json.JSONDecodeError as je:
            print(f"⚠️ Failed to parse recipe JSON: {je}")
            print(f"Response text: {text[:500]}...")

            # Return a minimal response if parsing fails
            return {
                "error": "Failed to parse recipe response",
                "raw_response": text[:1000],
            }

    except Exception as e:
        print(f"❌ Error in get_recipes_and_safety: {e}")
        import traceback

        traceback.print_exc()
        return {"error": str(e)}


def get_nutrition_and_impact(fruit_name, ripeness="ripe"):
    """
    Get nutritional information and environmental impact for a fruit.
    This doesn't require an image - just uses the fruit name.

    Args:
        fruit_name: Name of the fruit
        ripeness: Ripeness level (affects nutrition slightly)

    Returns:
        dict: Nutrition facts and environmental impact
    """
    try:
        print(f"📊 Getting nutrition info for {fruit_name} ({ripeness})...")

        prompt = f"""Provide nutritional information and environmental impact for a {ripeness} {fruit_name}.

Return data in this EXACT JSON format:
{{
  "fruit_name": "{fruit_name}",
  "serving_size": "1 medium (approx Xg)",
  "nutrition": {{
    "calories": 95,
    "carbs_g": 25,
    "fiber_g": 4,
    "sugar_g": 19,
    "protein_g": 1,
    "vitamin_c_percent": 17,
    "potassium_mg": 422
  }},
  "health_benefits": [
    "High in potassium for heart health",
    "Good source of vitamin B6",
    "Contains resistant starch when unripe"
  ],
  "environmental_impact": {{
    "carbon_footprint_kg": 0.7,
    "water_usage_liters": 790,
    "sustainability_rating": "medium",
    "local_season": "Year-round (imported)"
  }},
  "waste_reduction_tip": "Use overripe fruits in smoothies or freeze for later use"
}}

Be accurate with nutritional data. Environmental data should be realistic estimates."""

        response = model.generate_content(prompt)

        if not response or not hasattr(response, "text") or not response.text:
            return {"error": "No response from Gemini"}

        text = response.text.strip()
        text = re.sub(r"```json\s*", "", text)
        text = re.sub(r"```\s*", "", text)

        result = json.loads(text)
        print(f"✅ Nutrition data retrieved for {fruit_name}")
        return result

    except Exception as e:
        print(f"❌ Error in get_nutrition_and_impact: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # Test the service
    test_image_path = "../images/ripe_mango.jpg"
    if os.path.exists(test_image_path):
        with open(test_image_path, "rb") as image_file:
            image_bytes = image_file.read()

        print("Testing fruit name detection:")
        name_result = get_fruit_name(image_bytes)
        print(name_result)

        print("\nTesting ripeness analysis:")
        ripeness_result = analyze_ripeness_with_gemini(image_bytes)
        print(ripeness_result)

        print("\nTesting recipe suggestions:")
        recipe_result = get_recipes_and_safety(
            image_bytes,
            fruit_name=name_result.get("fruit_name"),
            ripeness=ripeness_result.get("ripeness"),
        )
        print(json.dumps(recipe_result, indent=2))

        print("\nTesting nutrition and impact:")
        nutrition_result = get_nutrition_and_impact(
            name_result.get("fruit_name"), ripeness_result.get("ripeness")
        )
        print(json.dumps(nutrition_result, indent=2))
