# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers as package imports
from backend.routes import predict, pantry, identify, storage

app = FastAPI(
    title="FreshCam",
    description="API for FreshCam",
    version="1.0.0",
    contact={
        "name": "FreshCam",
        "url": "https://github.com/DhruvParashar246/FreshCam",
        "email": "krishm.imp@gmail.com",
        "email2": "dhruvparashar246@gmail.com",
    },
)

# CORS (dev-friendly; tighten in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Mount routers. Adjust prefixes as you like.
# If your predict router already defines "/predict", prefix="" is fine.
app.include_router(predict.router, prefix="")       # e.g., POST /predict
app.include_router(pantry.router,  prefix="/pantry")# e.g., GET /pantry/items
app.include_router(identify.router, prefix="")      # e.g., POST /identify-fruit
app.include_router(storage.router, prefix="")       # e.g., POST /storage-advice
# If you prefer: app.include_router(identify.router, prefix="/ai")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
