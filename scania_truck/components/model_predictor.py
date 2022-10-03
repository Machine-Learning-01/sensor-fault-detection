from ast import Try
from scania_truck.components.data_ingestion import DataIngestion
from scania_truck.utils.read_params import read_params
from scania_truck.exception import ScaniaException
import logging
import sys
from scania_truck.cloud_storage.s3_operations import S3Operation

logger = logging.getLogger(__name__)


class ScaniaData:
    def __init__(self):

        self.data_ingestion = DataIngestion()

        self.config = read_params()
        
        self.target_column = self.config["target_column"]

        self.schema_config = self.config["schema_path"]

    def get_data(self):
        try:            
            test_set = self.data_ingestion.initiate_data_ingestion(test=True)


            return test_set

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message


class ScaniaTruckClassifier:
    def __init__(self):
        self.s3 = S3Operation()

        self.config = read_params()

        self.schema_config = self.config["schema_path"]

        self.drop_columns = self.schema_config["drop_columns"]

        self.target_column = self.config["target_column"]

        self.model_file = self.config["model_file_name"]

        self.io_files_bucket = self.config["s3_bucket"][
            "scania_truck_input_files_bucket"
        ]

    def predict(self, X):
        logging.info("Entered predict method of CarPricePredictor class")

        try:
            best_model = self.s3.load_model(self.model_file, self.io_files_bucket)

            logging.info("Loaded best model from s3 bucket")

            selling_price_pred = best_model.predict(X)

            logging.info("Used best model to get predictions")

            logging.info("Exited predict method of CarPricePredictor class")

            return selling_price_pred

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message
