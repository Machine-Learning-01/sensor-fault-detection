from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
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


# @app.get("/")
# async def predictGetRouteClient(request: Request):
#     try:
#         car_list = utils.get_car_list()

#         return templates.TemplateResponse(
#             "car_price.html",
#             {"request": request, "context": "Rendering", "car_list": car_list},
#         )

#     except Exception as e:
#         return Response(f"Error Occurred! {e}")


# @app.post("/")
# async def predictPostRouteClient(request: Request):
#     try:
#         form = DataForm(request)

#         await form.get_car_data()

#         car_price_data = CarPriceData(
#             car_name=form.car_name,
#             vehicle_age=form.vehicle_age,
#             km_driven=form.km_driven,
#             seller_type=form.seller_type,
#             fuel_type=form.fuel_type,
#             transmission_type=form.transmission_type,
#             mileage=form.mileage,
#             engine=form.engine,
#             max_power=form.max_power,
#             seats=form.seats,
#         )

#         carprice_df = car_price_data.get_car_data_as_dict()

#         carprice_predictor = CarPricePredictor()

#         car_list = utils.get_car_list()

#         carprice_value = carprice_predictor.predict(X=carprice_df)[0]

#         return templates.TemplateResponse(
#             "car_price.html",
#             {"request": request, "context": carprice_value, "car_list": car_list},
#         )

#     except Exception as e:
#         return {"status": False, "error": f"{e}"}


@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()

        train_pipeline.run_pipeline()

        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")



# @app.get("/predict")
# async def predictRouteClient():
#     try:
#         train_pipeline = TrainPipeline()

#         train_pipeline.run_pipeline()

#         return Response("Training successful !!")

#     except Exception as e:
#         return Response(f"Error Occurred! {e}")


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8080)
