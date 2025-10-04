from fastapi import FastAPI
from routes import predict, pantry

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

@app.get("/")
def test_route():
    return {"message": "Hello World"}

@app.get("/predict")
def predict_route():
    return predict.predict()

@app.get("/pantry")
def pantry_route():
    return pantry.pantry()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    