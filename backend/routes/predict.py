from fastapi import APIRouter, File, UploadFile
from services.cv_service import analyze_image

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File()):
    print("File size received:", len(image_bytes))
    image_bytes = await file.read()
    result = analyze_image(image_bytes)

    return result

