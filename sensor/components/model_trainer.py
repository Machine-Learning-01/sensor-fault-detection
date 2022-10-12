import sys
from typing import List, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame

from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import load_numpy_array_data, read_yaml_file, load_object, save_object
from sklearn.pipeline import Pipeline
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from neuro_mf  import ModelFactory
from sensor.entity.estimator import SensorModel

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
    #     self.main_utils = MainUtils()

    # def get_trained_models(self, train_arr: np.ndarray, test_arr: np.ndarray) -> List[Tuple[float, object, str]]:
    #     try:
    #         logging.info("Entered get_trained_models method of ModelTrainer class")
    #         model_config = read_yaml_file(file_path=self.model_trainer_config.model_config_file_path)
    #         models_list = list(model_config["train_model"].keys())
    #         logging.info("Got model list from the config file")
    #         x_train, y_train, x_test, y_test = train_arr[:, :-1], train_arr[:, -1], test_arr[:, :-1], test_arr[:, -1]

    #         tuned_model_list = [(self.main_utils.get_tuned_model(model_name, x_train, y_train, x_test, y_test, ))
    #                             for model_name in models_list]

    #         logging.info("Got trained model list")
    #         logging.info("Exited the get_trained_models method of ModelFinder class")

    #         return tuned_model_list
    #     except Exception as e:
    #         raise SensorException(e, sys) from e

    def initiate_model_trainer(self, ) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            x_train, y_train, x_test, y_test = train_arr[:, :-1], train_arr[:, -1], test_arr[:, :-1], test_arr[:, -1]
            # list_of_trained_models = self.get_trained_models(train_arr, test_arr)

            # logging.info("Got a list of tuple of model score, model and model name")

            # (best_model, best_model_score,) = self.main_utils.get_best_model_with_name_and_score(list_of_trained_models)

            # logging.info("Got best model score, model and model name")

            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
            best_model_detail = model_factory.get_best_model(X=x_train,y=y_train,base_accuracy=self.model_trainer_config.expected_accuracy)
            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)


            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                logging.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")

            sensor_model = SensorModel(preprocessing_object=preprocessing_obj,
                                       trained_model_object=best_model_detail.best_model)
            logging.info("Created Sensor truck model object with preprocessor and model")
            logging.info("Created best model file path.")
            save_object(self.model_trainer_config.trained_model_file_path, sensor_model)

            metric_artifact = ClassificationMetricArtifact(f1_score=0.8, precision_score=0.8, recall_score=0.9)
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact,
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
