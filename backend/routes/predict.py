from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from services.cv_service import analyze_image
from services.gemini_service import get_nutrition_and_impact, get_recipes_and_safety

router = APIRouter()


@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    include_recipes: bool = Query(
        default=False, description="Include recipe suggestions and food safety info"
    ),
    include_nutrition: bool = Query(
        default=True,
        description="Include nutritional information and environmental impact",
    ),
):
    """
    Analyze fruit image for ripeness detection.

    Args:
        file: Uploaded fruit image
        include_recipes: If true, also returns recipes, safety info, and shelf life
        include_nutrition: If true, includes nutrition facts and environmental impact

    Returns:
        Basic response:
        {
            "fruit_name": "apple",
            "ripeness": "ripe",
            "confidence": 92.5,
            "source": "cv_model",
            "nutrition": {...},
            "environmental_impact": {...}
        }

        With include_recipes=true:
        {
            "fruit_name": "apple",
            "ripeness": "ripe",
            "confidence": 92.5,
            "source": "cv_model",
            "is_safe_to_eat": true,
            "days_until_discard": 5,
            "storage_tips": "...",
            "recipes": [...],
            "nutrition": {...},
            "environmental_impact": {...}
        }
    """
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Read the file safely
        image_bytes = await file.read()
        print("✅ File size received:", len(image_bytes), "bytes")

        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        # Run CV model / Gemini for basic analysis
        result = analyze_image(image_bytes)
        print("✅ Analysis result:", result)

        # Get fruit info for additional features
        fruit_name = result.get("fruit_name", "unknown")
        ripeness = result.get("ripeness", "ripe")

        # Add nutrition and environmental impact (lightweight, no additional image processing)
        if include_nutrition and fruit_name != "unknown" and "error" not in result:
            print(f"📊 Fetching nutrition info for {fruit_name}...")
            nutrition_info = get_nutrition_and_impact(fruit_name, ripeness)

            if "error" not in nutrition_info:
                result.update(
                    {
                        "nutrition": nutrition_info.get("nutrition"),
                        "health_benefits": nutrition_info.get("health_benefits"),
                        "environmental_impact": nutrition_info.get(
                            "environmental_impact"
                        ),
                        "waste_reduction_tip": nutrition_info.get(
                            "waste_reduction_tip"
                        ),
                    }
                )
                print("✅ Added nutrition and impact data")

        # If recipes are requested, get additional info
        if include_recipes and "error" not in result:
            print("🍳 Fetching recipe suggestions...")
            recipe_info = get_recipes_and_safety(
                image_bytes,
                fruit_name=fruit_name,
                ripeness=ripeness,
            )

            if "error" not in recipe_info:
                # Merge recipe info into result
                result.update(
                    {
                        "is_safe_to_eat": recipe_info.get("is_safe_to_eat"),
                        "days_until_discard": recipe_info.get("days_until_discard"),
                        "storage_tips": recipe_info.get("storage_tips"),
                        "recipes": recipe_info.get("recipes", []),
                    }
                )
                print(
                    f"✅ Added {len(recipe_info.get('recipes', []))} recipes to response"
                )
            else:
                print(f"⚠️ Failed to get recipes: {recipe_info.get('error')}")

        return result

    except Exception as e:
        print("❌ Error in /predict:", e)
        raise HTTPException(status_code=500, detail=str(e))
