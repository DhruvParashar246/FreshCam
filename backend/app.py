from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import predict, recipes

app = FastAPI(
    title="FreshCam - AI-Powered Fruit Freshness & Recipe Assistant",
    description="Reduce food waste with AI-powered fruit analysis, ripeness detection, recipe suggestions, and food safety insights",
    version="1.0.0",
    contact={
        "name": "FreshCam Team",
        "url": "https://github.com/DhruvParashar246/FreshCam",
        "email": "krishm.imp@gmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def test_route():
    return {
        "message": "FreshCam API - AI-Powered Fruit Analysis",
        "version": "1.0.0",
        "endpoints": {
            "POST /predict": "Analyze fruit ripeness",
            "POST /predict?include_recipes=true": "Analyze fruit + get recipes",
            "POST /recipes": "Get recipe suggestions and food safety info",
            "GET /docs": "Interactive API documentation",
        },
    }


app.include_router(predict.router)
app.include_router(recipes.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
