import logging
import sys

from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_transformation import DataTransformation
from sensor.components.data_validation import DataValidation
from sensor.components.model_trainer import ModelTrainer
from sensor.exception import SensorException
from sensor.utils.main_utils import MainUtils
from sensor.utils.read_params import read_params

logger = logging.getLogger(__name__)


class TrainPipeline:
    def __init__(self):
        self.config = read_params()

        self.utils = MainUtils()

        self.artifacts_dir = self.config["artifacts_dir"]

    def start_data_ingestion(self):
        logger.info("Entered the start_data_ingestion method of TrainPipeline class")

        try:
            logging.info("Getting the data from mongodb")

            data_ingestion = DataIngestion()

            train_data, test_set = data_ingestion.initiate_data_ingestion()

            logging.info("Got the train_set and test_set from mongodb")

            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return train_data, test_set

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def start_data_validation(train_set, test_set):
        logger.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(train_set, test_set)

            data_validation_status = data_validation.initiate_data_validation()

            logger.info("Performed the data validation operation")

            logger.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_status

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def start_data_transformation(train_set, test_set):
        logger.info(
            "Entered the start_data_transformation method of TrainPipeline class"
        )

        try:
            data_transformation = DataTransformation()

            train_set, test_set = data_transformation.initiate_data_transformation(
                train_set, test_set
            )

            logger.info(
                "Exited the start_data_transformation method of TrainPipeline class"
            )

            return train_set, test_set

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def start_model_pusher():
        logger.info("Entered the start_model_pusher method of TrainPipeline class")

        try:
            model_trainer = ModelTrainer()

            model_trainer.initiate_model_pusher()

            logger.info("Initiated the model pusher")

            logger.info("Exited the start_model_pusher method of TrainPipeline class")

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def start_model_trainer(train_set, test_set):
        logger.info("Entered the start_model_trainer method of TrainPipeline class")

        try:
            model_trainer = ModelTrainer()

            model_trainer.initiate_model_trainer(train_set, test_set)

            logger.info("Exited the start_model_trainer method of TrainPipeline class")

        except Exception as e:
            raise SensorException(e, sys) from e

    def run_pipeline(self):
        logger.info("Entered the run_pipeline method of TrainPipeline class")

        try:
            train_set, test_set = self.start_data_ingestion()

            if self.start_data_validation(train_set, test_set):
                train_set, test_set = self.start_data_transformation(
                    train_set, test_set
                )

                self.start_model_trainer(train_set, test_set)

                self.start_model_pusher()

            logger.info("Exited the run_pipeline method of TrainPipeline class")

        except Exception as e:
            raise SensorException(e, sys) from e
