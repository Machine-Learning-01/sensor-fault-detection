import logging
import sys

from pandas import DataFrame

from sensor.cloud_storage.s3_operations import S3Operation
from sensor.components.data_ingestion import DataIngestion
from sensor.exception import SensorException
from sensor.utils.read_params import read_params

logger = logging.getLogger(__name__)


class SensorData:
    def __init__(self):
        self.data_ingestion = DataIngestion()

        self.config = read_params()

        self.schema_config = read_params("sensor/config/schema.yaml")

        self.pred_data_csv_file = self.config["pred_data_csv_file"]

        self.pred_data_bucket = self.config["s3_bucket"]["sensor_pred_bucket"]

        self.drop_columns = self.schema_config["drop_columns"]

        self.s3 = S3Operation()

    def get_data(self):
        logger.info("Entered get_data method of SensorData class")
        try:
            pred_df = self.s3.read_csv(self.pred_data_csv_file, self.pred_data_bucket)

            logger.info("Read prediction csv file from s3 bucket")

            pred_df = pred_df.drop(self.drop_columns, axis=1)

            logger.info("Dropped the required columns")

            logger.info("Exited the get_data method of SensorData class")

            return pred_df

        except Exception as e:
            raise SensorException(e, sys) from e


class SensorClassifier:
    def __init__(self):
        self.s3 = S3Operation()

        self.config = read_params()

        self.model_file = self.config["model_file_name"]

        self.io_files_bucket = self.config["s3_bucket"]["sensor_input_files_bucket"]

        self.predictions_file = self.config["predictions_file"]

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
                result,
                self.predictions_file,
                self.predictions_file,
                self.io_files_bucket,
            )

            logging.info(
                "Used best model to get predictions and prediction are stored in io files bucket"
            )

            logging.info("Exited predict method of CarPricePredictor class")

        except Exception as e:
            raise SensorException(e, sys) from e
