from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from uvicorn import run as app_run

from sensor.components.model_predictor import SensorClassifier
from sensor.constant import APP_HOST, APP_PORT
from sensor.pipeline.train_pipeline import TrainPipeline

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()

        train_pipeline.run_pipeline()

        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.get("/predict")
async def predictRouteClient():
    try:
        model_predictor = SensorClassifier()

        model_predictor.predict()

        return Response(
            "Prediction successful and predictions are stored in s3 bucket !!"
        )

    except Exception as e:
        return Response(f"Error Occurred! {e}")


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
