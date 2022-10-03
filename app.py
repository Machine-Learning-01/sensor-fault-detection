from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from uvicorn import run as app_run
from fastapi import FastAPI

from scania_truck.pipeline.train_pipeline import TrainPipeline
from scania_truck.utils.read_params import read_params

app = FastAPI()

config = read_params()


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

if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8080)
