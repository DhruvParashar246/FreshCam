from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/pantry")
def pantry():
    return {"message": "Pantry..."}