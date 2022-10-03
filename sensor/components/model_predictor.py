from sensor.components.data_ingestion import DataIngestion
from sensor.utils.read_params import read_params
from sensor.exception import SensorException
import logging
import sys
from pandas import DataFrame
from sensor.cloud_storage.s3_operations import S3Operation

logger = logging.getLogger(__name__)


class SensorData:
    def __init__(self):
        self.data_ingestion = DataIngestion()

        self.config = read_params()

        self.schema_config = self.config["schema_path"]

        self.pred_data_csv_file = self.config["pred_data_csv_file"]

        self.pred_data_bucket = self.config["s3_bucket"]["Sensor-truck-pred_bucket"]

        self.drop_columns = self.schema_config["drop_columns"]

        self.s3 = S3Operation()

    def get_data(self):
        try:
            pred_df = self.s3.read_csv(self.pred_data_csv_file, self.pred_data_bucket)

            pred_df = pred_df.drop(self.drop_columns, axis=1)

            return pred_df

        except Exception as e:
            message = SensorException(e, sys)
            raise message.error_message


class SensorTruckClassifier:
    def __init__(self):
        self.s3 = S3Operation()

        self.config = read_params()

        self.model_file = self.config["model_file_name"]

        self.io_files_bucket = self.config["s3_bucket"][
            "Sensor_truck_input_files_bucket"
        ]

        self.pred_data = SensorData()

    def predict(self):
        logging.info("Entered predict method of CarPricePredictor class")

        try:
            X = self.pred_data.get_data()

            best_model = self.s3.load_model(self.model_file, self.io_files_bucket)

            logging.info("Loaded best model from s3 bucket")

            result = list(best_model.predict(X))

            result = DataFrame(list((result)), columns=["Prediction"])

            self.s3.upload_df_as_csv(
                result, "Sensor_results.csv", "Sensor_results.csv", "Sensor-io-files"
            )

            logging.info(
                "Used best model to get predictions and prediction are stored in io files bucket"
            )

            logging.info("Exited predict method of CarPricePredictor class")

        except Exception as e:
            message = SensorException(e, sys)
            raise message.error_message
