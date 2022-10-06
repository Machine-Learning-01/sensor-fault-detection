<<<<<<< HEAD
import logging
import sys

from pandas import DataFrame

from sensor.cloud_storage.s3_operations import S3Operation
from sensor.components.data_ingestion import DataIngestion
from sensor.exception import SensorException
from sensor.utils.read_params import read_params
=======
import sys
>>>>>>> 04af0a7d267aa1f662cd5855e3b5b2c11d6fe4db

from pandas import DataFrame

from sensor.cloud_storage.s3_operations import S3Operation
from sensor.components.data_ingestion import DataIngestion
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import MainUtils


class SensorData:
    def __init__(self):
        self.data_ingestion = DataIngestion()

        self.utils = MainUtils()

        self.schema_config = self.utils.read_schema_config_file()

<<<<<<< HEAD
        self.pred_data_csv_file = self.config["pred_data_csv_file"]
=======
        # self.pred_data_csv_file = self.config["pred_data_csv_file"]

        # self.pred_data_bucket = self.config["s3_bucket"]["sensor_pred_bucket"]
>>>>>>> 04af0a7d267aa1f662cd5855e3b5b2c11d6fe4db

        # self.drop_columns = self.schema_config["drop_columns"]

        self.s3 = S3Operation()

    def get_data(self):
        logging.info("Entered get_data method of SensorData class")
        try:
            pred_df = self.s3.read_csv(self.pred_data_csv_file, self.pred_data_bucket)

<<<<<<< HEAD
            logger.info("Read prediction csv file from s3 bucket")
=======
            logging.info("Read prediction csv file from s3 bucket")
>>>>>>> 04af0a7d267aa1f662cd5855e3b5b2c11d6fe4db

            pred_df = pred_df.drop(self.drop_columns, axis=1)

            logging.info("Dropped the required columns")

            logging.info("Exited the get_data method of SensorData class")

<<<<<<< HEAD
            logger.info("Exited the get_data method of SensorData class")

=======
>>>>>>> 04af0a7d267aa1f662cd5855e3b5b2c11d6fe4db
            return pred_df

        except Exception as e:
            raise SensorException(e, sys) from e


class SensorClassifier:
    def __init__(self):
        self.s3 = S3Operation()

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
