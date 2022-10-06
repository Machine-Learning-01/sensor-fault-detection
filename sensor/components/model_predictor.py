import logging
import sys

from pandas import DataFrame

from sensor.components.data_ingestion import DataIngestion
from sensor.configuration.s3_operations import S3Operation
from sensor.constant import MODEL_FILE_NAME, PRED_DATA_CSV_FILE, PREDICTIONS_FILE
from sensor.entity.config_entity import S3Config
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import MainUtils


class SensorData:
    def __init__(self):
        self.data_ingestion = DataIngestion()

        self.utils = MainUtils()

        self.schema_config = self.utils.read_schema_config_file()

        self.s3_config = S3Config()

        self.s3 = S3Operation()

    def get_data(self):
        logging.info("Entered get_data method of SensorData class")

        try:
            pred_df = self.s3.read_csv(
                PRED_DATA_CSV_FILE, self.s3_config.PRED_DATA_BUCKET
            )

            logging.info("Read prediction csv file from s3 bucket")

            pred_df = pred_df.drop(self.schema_config["drop_columns"], axis=1)

            logging.info("Dropped the required columns")

            logging.info("Exited the get_data method of SensorData class")

            return pred_df

        except Exception as e:
            raise SensorException(e, sys) from e


class SensorClassifier:
    def __init__(self):
        self.s3 = S3Operation()

        self.s3_config = S3Config()

        self.pred_data = SensorData()

    def predict(self) -> None:
        logging.info("Entered predict method of CarPricePredictor class")

        try:
            X = self.pred_data.get_data()

            best_model = self.s3.load_model(
                MODEL_FILE_NAME, self.s3_config.IO_FILES_BUCKET
            )

            logging.info("Loaded best model from s3 bucket")

            result = list(best_model.predict(X))

            result = DataFrame(list((result)), columns=["Prediction"])

            self.s3.upload_df_as_csv(
                result,
                PREDICTIONS_FILE,
                PREDICTIONS_FILE,
                self.s3_config.IO_FILES_BUCKET,
            )

            logging.info(
                "Used best model to get predictions and prediction are stored in io files bucket"
            )

            logging.info("Exited predict method of CarPricePredictor class")

        except Exception as e:
            raise SensorException(e, sys) from e
