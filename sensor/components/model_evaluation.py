from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.entity.artifact_entity import ModelTrainerArtifact, DataIngestionArtifact, ModelEvaluationArtifact
from sensor.utils.main_utils import load_object
from sklearn.metrics import f1_score
from sensor.exception import SensorException
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.logger import logging
import os, sys
import pandas as pd
from typing import Dict
from sensor.entity.s3_estimator import SensorEstimator
from dataclasses import dataclass


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float


class ModelEvaluation:

    def __init__(self, model_eval_config: ModelEvaluationConfig, data_ingestion_artifact: DataIngestionArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys) from e

    def get_best_model(self) -> SensorEstimator:
        try:
            sensor_estimator = SensorEstimator(bucket_name=self.model_trainer_artifact.bucket_name,
                                               model_path=self.model_eval_config.model_path)

            return sensor_estimator
        except Exception as e:
            raise  SensorException(e,sys)

    def evaluate_model(self) -> EvaluateModelResponse:
        try:
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            x, y = test_df.drop(TARGET_COLUMN, axis=1), test_df[TARGET_COLUMN]

            best_model = self.get_best_model()
            trained_model = load_object(file_path=self.model_trainer_artifact.trained_model_file_path)

            y_hat_best_model = best_model.predict(x)
            y_hat_trained_model = trained_model.predict(x)

            trained_model_f1_score = f1_score(y, y_hat_trained_model)
            best_model_f1_score = f1_score(y, y_hat_best_model)

            # calucate how much percentage training model accuracy is increased/decreased

            result = EvaluateModelResponse(trained_model_f1_score=trained_model_f1_score,
                                           best_model_f1_score=best_model_f1_score,
                                           is_model_accepted=trained_model_f1_score > best_model_f1_score,
                                           difference=trained_model_f1_score - best_model_f1_score
                                           )
            logging.info(f"Result: {result}")
            return result

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            evaluate_model_response = self.evaluate_model()
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                best_model_path=self.model_trainer_artifact.trained_model_file_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=evaluate_model_response.difference)

            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
