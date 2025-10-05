from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from backend.services.gemini_service import identify_fruit

router = APIRouter()

class Alt(BaseModel):
    fruit: str
    confidence: float = Field(ge=0.0, le=1.0)

class IdentifyResponse(BaseModel):
    fruit: str
    confidence: float = Field(ge=0.0, le=1.0)
    alternatives: List[Alt] = []
    reason: Optional[str] = None
    raw: Optional[str] = None   # optional for debugging

@router.post("/identify-fruit", response_model=IdentifyResponse)
async def identify_fruit_route(file: UploadFile = File(...), debug: bool = False):
    try:
        data = await file.read()
        parsed, raw = identify_fruit(data, file.content_type or "image/jpeg")

        # normalize fields
        fruit = str(parsed.get("fruit", "unknown")).lower().strip()
        conf = float(parsed.get("confidence", 0.0))
        alts_in = parsed.get("alternatives", []) or []
        alts = []
        for a in alts_in[:3]:
            try:
                alts.append(Alt(fruit=str(a.get("fruit", "")).lower().strip(),
                                confidence=float(a.get("confidence", 0.0))))
            except Exception:
                continue

        resp = IdentifyResponse(
            fruit=fruit,
            confidence=max(0.0, min(conf, 1.0)),
            alternatives=alts,
            reason=parsed.get("reason"),
            raw=raw if debug else None,
        )
        return resp
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"gemini error: {e}")
