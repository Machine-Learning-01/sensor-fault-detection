import sys

from sensor.entity.artifact_entity import ModelPusherArtifact, ModelTrainerArtifact
from sensor.entity.config_entity import ModelPusherConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.ml.model.s3_estimator import SensorEstimator


class ModelPusher:
    def __init__(
        self,
        model_trainer_artifact: ModelTrainerArtifact,
        model_pusher_config: ModelPusherConfig,
    ):
        self.model_trainer_artifact = model_trainer_artifact

        self.model_pusher_config = model_pusher_config

        self.sensor_estimator = SensorEstimator(
            bucket_name=model_pusher_config.bucket_name,
            model_path=model_pusher_config.s3_model_key_path,
        )

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        logging.info("Entered initiate_model_pusher method of ModelTrainer class")

        try:
            logging.info("Uploading artifacts folder to s3 bucket")

            self.sensor_estimator.save_model(
                from_file=self.model_trainer_artifact.trained_model_file_path
            )

            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path,
            )

            logging.info("Uploaded artifacts folder to s3 bucket")

            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")

            logging.info("Exited initiate_model_pusher method of ModelTrainer class")

            return model_pusher_artifact

        except Exception as e:
            raise SensorException(e, sys) from e
