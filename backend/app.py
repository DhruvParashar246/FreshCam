from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import pantry

app = FastAPI(
    title="FreshCam API",
    description="Backend API for FreshCam - AI-powered food freshness detection",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pantry.router)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "FreshCam API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "services": {
            "pantry": "active",
            "database": "connected"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
