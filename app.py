from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

config = read_params()

templates = Jinja2Templates(directory=config["templates"]["dir"])


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


CAR_DATA_KEY = "carprice_data"

CAR_VALUE_KEY = "carprice_value"

utils = MainUtils()


class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request

        self.car_name: Optional[str] = None

        self.vehicle_age: Optional[str] = None

        self.km_driven: Optional[str] = None

        self.seller_type: Optional[str] = None

        self.fuel_type: Optional[str] = None

        self.transmission_type: Optional[str] = None

        self.mileage: Optional[str] = None

        self.engine: Optional[str] = None

        self.max_power: Optional[str] = None

        self.seats: Optional[str] = None

    async def get_car_data(self):
        form = await self.request.form()

        self.car_name = form.get("car_name")

        self.vehicle_age = form.get("vehicle_age")

        self.km_driven = form.get("km_driven")

        self.seller_type = form.get("seller_type")

        self.fuel_type = form.get("fuel_type")

        self.transmission_type = form.get("transmission")

        self.mileage = form.get("mileage")

        self.engine = form.get("engine")

        self.max_power = form.get("max_power")

        self.seats = form.get("seats")


@app.get("/")
async def predictGetRouteClient(request: Request):
    try:
        car_list = utils.get_car_list()

        return templates.TemplateResponse(
            "car_price.html",
            {"request": request, "context": "Rendering", "car_list": car_list},
        )

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/")
async def predictPostRouteClient(request: Request):
    try:
        form = DataForm(request)

        await form.get_car_data()

        car_price_data = CarPriceData(
            car_name=form.car_name,
            vehicle_age=form.vehicle_age,
            km_driven=form.km_driven,
            seller_type=form.seller_type,
            fuel_type=form.fuel_type,
            transmission_type=form.transmission_type,
            mileage=form.mileage,
            engine=form.engine,
            max_power=form.max_power,
            seats=form.seats,
        )

        carprice_df = car_price_data.get_car_data_as_dict()

        carprice_predictor = CarPricePredictor()

        car_list = utils.get_car_list()

        carprice_value = carprice_predictor.predict(X=carprice_df)[0]

        return templates.TemplateResponse(
            "car_price.html",
            {"request": request, "context": carprice_value, "car_list": car_list},
        )

    except Exception as e:
        return {"status": False, "error": f"{e}"}


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
        train_pipeline = TrainPipeline()

        train_pipeline.run_pipeline()

        return Response("Training successful !!")
    
    except Exception as e:
        return Response(f"Error Occurred! {e}") 


if __name__ == "__main__":
    app_run(app, host=config["app"]["host"], port=config["app"]["port"])