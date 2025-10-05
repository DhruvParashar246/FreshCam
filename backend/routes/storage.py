from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from backend.services.gemini_service import identify_fruit_from_file
from backend.services.gemini_storage import generate_storage_advice

router = APIRouter()


class StorageRequest(BaseModel):
    fruit: str = Field(..., description="Common fruit name, e.g. 'apple'")
    ripeness: Optional[str] = Field(None, description="Optional ripeness like 'ripe' or 'unripe'")
    quantity: Optional[int] = Field(None, description="Optional number of pieces")


class StorageResponse(BaseModel):
    fruit: str
    advice: str
    raw: Optional[str] = None


@router.post("/storage-advice", response_model=StorageResponse)
async def storage_advice(req: StorageRequest, debug: bool = False):
    try:
        # Call the gemini storage helper which returns (advice_text, raw)
        advice_text, raw = generate_storage_advice(req.fruit, ripeness=req.ripeness, quantity=req.quantity)

        return StorageResponse(fruit=req.fruit.lower(), advice=advice_text, raw=raw if debug else None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"storage advice error: {e}")
