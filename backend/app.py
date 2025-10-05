from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import predict

app = FastAPI(
    title="FreshCam",
    description="API for FreshCam",
    version="1.0.0",
    contact={
        "name": "FreshCam",
        "url": "https://github.com/DhruvParashar246/FreshCam",
        "email": "krishm.imp@gmail.com",
        "email2": "dhruvparashar246@gmail.com",
    }
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
    return {"message": "Hello World"}

app.include_router(predict.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    