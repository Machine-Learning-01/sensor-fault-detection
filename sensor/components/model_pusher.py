import sys

from sensor.configuration.s3_operations import S3Operation
from sensor.constant import BEST_MODEL_PATH, PREPROCESSOR_OBJ_FILE_NAME
from sensor.entity.config_entity import S3Config
from sensor.exception import SensorException
from sensor.logger import logging


class ModelPusher:
    def __init__(self):
        self.s3 = S3Operation()

        self.s3_config = S3Config()

    def initiate_model_pusher(self) -> None:
        logging.info("Entered initiate_model_pusher method of ModelTrainer class")

        try:
            logging.info("Uploading artifacts folder to s3 bucket")

            self.s3.upload_file(
                BEST_MODEL_PATH, BEST_MODEL_PATH, self.s3_config.IO_FILES_BUCKET
            )

            self.s3.upload_file(
                PREPROCESSOR_OBJ_FILE_NAME,
                PREPROCESSOR_OBJ_FILE_NAME,
                self.s3_config.IO_FILES_BUCKET,
            )

            logging.info("Uploaded artifacts folder to s3 bucket")

            logging.info("Exited initiate_model_pusher method of ModelTrainer class")

        except Exception as e:
            raise SensorException(e, sys) from e
