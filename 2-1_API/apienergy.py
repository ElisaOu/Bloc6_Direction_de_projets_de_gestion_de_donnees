# Importing libraries
import mlflow 
import uvicorn
import json
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
from joblib import load
import os

# 2 suivants chez inspi K
import boto3
import pickle

description = """
Here is our app of machine learning predicting consommation of electricity in France!
Check out documentation below 👇 for more information on each endpoint. 
"""


tags_metadata = [
    {
        "name": "Introduction Endpoint",
        "description": "Simple endpoint to try out!",
    },

    {
        "name": "Machine Learning Endpoint",
        "description": "Electricity consumption estimation"
    }
]


app = FastAPI(
    title="Estimation of electricity consumption",
    description=description,
    version="0.1",
    contact={
        "name": "Predict electricity consumption: Watt a job!",
        #"url": "none",
    },
    openapi_tags=tags_metadata
)


class PredictionFeatures(BaseModel):
    Nom_region: str = 'ILE DE FRANCE'
    lag_1: float = 475000
    lag_2: float = 500000
    lag_3: float = 430000
    lag_4: float = 420000
    lag_5: float = 460000
    lag_6: float = 450000
    lag_7: float = 400000
    lag_8: float = 450000
    lag_9: float = 470000
    lag_10: float = 450000
    lag_11: float = 480000
    lag_12: float = 470000
    lag_13: float = 500000
    lag_14: float = 510000
    lag_15: float = 520000
    lag_364: float = 400000
    #rolling_mean_7: float=450000
    #rolling_mean_15: float=470000
    #temp_max: float=9
    #temp_min: float=5
    #hours_of_sun: float=2
    #precipitation: float=3
    #windspeed: float=22
    #prix_kwh_elec: float=0.15
    #prix_gaz: float=33.4
    #brent_price: float=82
    day: int = 2
    year: int = 2023
    month: int = 1
    day_of_week: int = 0


@app.get("/", tags=["Introduction Endpoint"])
async def index():

    message = 'This is the API default endpoint. To get more information about the API, go to "/docs".'
    return message



@app.post("/predict", tags=["Machine Learning Endpoint"])
async def predict(features: PredictionFeatures):
    """
    Estimation electricity consumption.
    """
    # Read data 
    df = pd.DataFrame(dict(features), index=[0])

    # Log model from mlflow 
    #logged_model = 'runs:/36242416f2f64dc080ab07ac1d8abfe0/Energy' # A METTRE A JOUR

    # Load model as a PyFuncModel.
    #loaded_model = mlflow.pyfunc.load_model(logged_model)

    # If you want to load model persisted locally
    loaded_model = load('elec.joblib')

    prediction = loaded_model.predict(df)

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000) # Here you define your web server to run the `app` variable 
                                    # (which contains FastAPI instance), with a specific host IP (0.0.0.0) and port (4000)