import certifi
ca=certifi.where()
import os
import sys
from io import StringIO
from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
import networksecurity.logging as logger
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response, JSONResponse
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

app = FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successfully completed!")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))
        # x = df.values()
        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])
        model = load_object("final_model/model.pkl")
        preprocessor = load_object("final_model/preprocessor.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=model)
        predictions = network_model.predict(df)

        return JSONResponse(content={"predictions": predictions.tolist()})
    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)