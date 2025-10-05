from fastapi import APIRouter, File, UploadFile, HTTPException
from services.cv_service import analyze_image

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # ✅ Read the file safely
        image_bytes = await file.read()
        print("✅ File size received:", len(image_bytes), "bytes")

        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        # ✅ Run CV model
        result = analyze_image(image_bytes)
        print("✅ Analysis result:", result)
        return result

    except Exception as e:
        print("❌ Error in /predict:", e)
        raise HTTPException(status_code=500, detail=str(e))
