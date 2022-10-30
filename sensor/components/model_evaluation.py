import sys
from typing import Optional

import pandas as pd
from sklearn.metrics import f1_score

from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.entity.artifact_entity import (
    ClassificationMetricArtifact,
    DataValidationArtifact,
    ModelEvaluationArtifact,
    ModelTrainerArtifact,
)
from sensor.entity.config_entity import EvaluateModelResponse, ModelEvaluationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.ml.metric import calculate_metric
from sensor.ml.model.estimator import TargetValueMapping
from sensor.ml.model.s3_estimator import SensorEstimator
from sensor.utils.main_utils import load_object


class ModelEvaluation:
    def __init__(
        self,
        model_eval_config: ModelEvaluationConfig,
        data_validation_artifact: DataValidationArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
    ):
        try:
            self.model_eval_config = model_eval_config

            self.data_validation_artifact = data_validation_artifact

            self.model_trainer_artifact = model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys) from e

    def get_best_model(self) -> Optional[SensorEstimator]:
        try:
            bucket_name = self.model_eval_config.bucket_name

            model_path = self.model_eval_config.s3_model_key_path

            sensor_estimator = SensorEstimator(
                bucket_name=bucket_name, model_path=model_path
            )

            if sensor_estimator.is_model_present(model_path=model_path):
                return sensor_estimator

            return None

        except Exception as e:
            raise SensorException(e, sys)

    def evaluate_model(self) -> EvaluateModelResponse:
        try:
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)

            x, y = test_df.drop(TARGET_COLUMN, axis=1), test_df[TARGET_COLUMN]

            trained_model = load_object(
                file_path=self.model_trainer_artifact.trained_model_file_path
            )

            y.replace(TargetValueMapping().to_dict(), inplace=True)

            y_hat_trained_model = trained_model.predict(x)

            trained_model_score = calculate_metric(
                trained_model, y, y_hat_trained_model
            )

            trained_model_f1_score = trained_model_score.f1_score

            best_model_f1_score = None

            best_model_metric_artifact = None

            best_model = self.get_best_model()

            if best_model is not None:
                best_model_metric_artifact = calculate_metric(best_model, x, y)

                best_model_f1_score = best_model_metric_artifact.f1_score

            # calucate how much percentage training model accuracy is increased/decreased
            tmp_best_model_score = (
                0 if best_model_f1_score is None else best_model_f1_score
            )

            result = EvaluateModelResponse(
                trained_model_f1_score=trained_model_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted=trained_model_f1_score > tmp_best_model_score,
                changed_accuracy=trained_model_f1_score - tmp_best_model_score,
                best_model_metric_artifact=best_model_metric_artifact,
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
                changed_accuracy=evaluate_model_response.changed_accuracy,
                best_model_metric_artifact=evaluate_model_response.best_model_metric_artifact,
            )

            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")

            return model_evaluation_artifact

        except Exception as e:
            raise SensorException(e, sys) from e
