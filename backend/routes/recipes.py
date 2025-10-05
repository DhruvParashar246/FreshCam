from fastapi import APIRouter, File, HTTPException, UploadFile
from services.gemini_service import (
    analyze_ripeness_with_gemini,
    get_fruit_name,
    get_recipes_and_safety,
)

router = APIRouter()


@router.post("/recipes")
async def get_recipes(file: UploadFile = File(...)):
    """
    Get recipe suggestions, food safety info, and shelf life for a fruit.

    This endpoint analyzes the uploaded fruit image and returns:
    - Recipe suggestions optimized for the fruit's ripeness
    - Food safety assessment
    - Estimated days until the fruit should be discarded
    - Storage tips to maximize freshness
    """
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Read the file
        image_bytes = await file.read()
        print(f"✅ Recipe request - File size: {len(image_bytes)} bytes")

        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        # First detect fruit name and ripeness for better context
        print("📊 Detecting fruit and ripeness first...")
        fruit_info = get_fruit_name(image_bytes)
        ripeness_info = analyze_ripeness_with_gemini(image_bytes)

        fruit_name = fruit_info.get("fruit_name", "unknown")
        ripeness = ripeness_info.get("ripeness", "unknown")

        print(f"   Detected: {fruit_name} ({ripeness})")

        # Get recipes and safety info
        result = get_recipes_and_safety(
            image_bytes, fruit_name=fruit_name, ripeness=ripeness
        )

        if "error" in result:
            print(f"❌ Error in recipe generation: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        print("✅ Recipe suggestions generated successfully")
        return result

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in /recipes endpoint: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
