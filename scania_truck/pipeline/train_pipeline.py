import logging
import sys

from scania_truck.components.data_ingestion import DataIngestion
from scania_truck.components.data_transformation import DataTransformation
from scania_truck.components.data_validation import DataValidation
from scania_truck.components.model_trainer import ModelTrainer
from scania_truck.exception import ScaniaException
from scania_truck.utils.main_utils import MainUtils
from scania_truck.utils.read_params import read_params

logger = logging.getLogger(__name__)


class TrainPipeline:
    def __init__(self):
        self.config = read_params()

        self.utils = MainUtils()

        self.artifacts_dir = self.config["artifacts_dir"]

    def start_data_ingestion(self):
        logger.info("Entered the start_data_ingestion method of Pipeline class")

        try:
            logging.info("Getting the data from mongodb")

            data_ingestion = DataIngestion()
            
            train_data,test_set = data_ingestion.initiate_data_ingestion()
            
            return train_data,test_set

        except Exception as e:
            message = ScaniaException(e, sys)
            raise message.error_message

    @staticmethod
    def start_data_validation(train_set, test_set):
        try:
            data_validation = DataValidation(train_set, test_set)

            return data_validation.initiate_data_validation()

        except Exception as e:
            message = ScaniaException(e, sys)
            raise message.error_message

    @staticmethod
    def start_data_transformation(train_set, test_set):
        try:
            data_transformation = DataTransformation()

            train_set, test_set = data_transformation.initiate_data_transformation(
                train_set, test_set
            )

            logger.info("Exited the start_data_transformation method of Pipeline class")

            return train_set, test_set

        except Exception as e:
            message = ScaniaException(e, sys)
            raise message.error_message

    @staticmethod
    def start_model_pusher():
        try:
            model_trainer = ModelTrainer()

            model_trainer.initiate_model_pusher()

        except Exception as e:
            message = ScaniaException(e, sys)
            raise message.error_message

    @staticmethod
    def start_model_trainer(train_set, test_set):
        try:
            model_trainer = ModelTrainer()

            model_trainer.initiate_model_trainer(train_set, test_set)

        except Exception as e:
            message = ScaniaException(e, sys)
            raise message.error_message

    def run_pipeline(self):
        try:
            train_set, test_set = self.start_data_ingestion()

            if self.start_data_validation(train_set, test_set):
                train_set, test_set = self.start_data_transformation(
                    train_set, test_set
                )

                self.start_model_trainer(train_set, test_set)

                self.start_model_pusher()

        except Exception as e:
            message = ScaniaException(e, sys)
            raise message.error_message
