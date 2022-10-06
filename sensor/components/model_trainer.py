import sys
from typing import List, Tuple

from pandas import DataFrame

from sensor.configuration.s3_operations import S3Operation
from sensor.constant import BEST_MODEL_PATH, PREPROCESSOR_OBJ_FILE_NAME
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import MainUtils


class SensorModel:
    def __init__(self, preprocessing_object: object, trained_model_object: object):
        self.preprocessing_object = preprocessing_object

        self.trained_model_object = trained_model_object

    def predict(self, X: DataFrame) -> DataFrame:
        logging.info("Entered predict method of SensorTruckModel class")

        try:
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(X)

            logging.info("Used the trained model to get predictions")

            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise SensorException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class ModelTrainer:
    def __init__(self):
        self.utils = MainUtils()

        self.s3 = S3Operation()

    def get_trained_models(
        self, X_data: DataFrame, Y_data: DataFrame
    ) -> List[Tuple[float, object, str]]:

        logging.info("Entered get_trained_models method of ModelTrainer class")

        try:
            model_config = self.utils.read_model_config_file()

            models_list = list(model_config["train_model"].keys())

            logging.info("Got model list from the config file")

            x_train, y_train, x_test, y_test = (
                X_data[:, :-1],
                X_data[:, -1],
                Y_data[:, :-1],
                Y_data[:, -1],
            )

            tuned_model_list = [
                (
                    self.utils.get_tuned_model(
                        model_name, x_train, y_train, x_test, y_test,
                    )
                )
                for model_name in models_list
            ]

            logging.info("Got trained model list")

            logging.info("Exited the get_trained_models method of ModelFinder class")

            return tuned_model_list

        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_model_trainer(self, train_set: DataFrame, test_set: DataFrame) -> None:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            list_of_trained_models = self.get_trained_models(train_set, test_set)

            logging.info("Got a list of tuple of model score, model and model name")

            (
                best_model,
                best_model_score,
            ) = self.utils.get_best_model_with_name_and_score(list_of_trained_models)

            logging.info("Got best model score, model and model name")

            preprocessing_obj = self.utils.load_object(PREPROCESSOR_OBJ_FILE_NAME)

            _model_config = self.utils.read_model_config_file()

            logging.info("Loaded preprocessing object")

            base_model_score = float(_model_config["base_model_score"])

            if best_model_score >= base_model_score:
                self.utils.update_model_score(best_model_score)

                logging.info("Updating model score in yaml file")

                sensor_model = SensorModel(preprocessing_obj, best_model)

                logging.info(
                    "Created Sensor truck model object with preprocessor and model"
                )

                logging.info("Created best model file path.")

                self.utils.save_object(BEST_MODEL_PATH, sensor_model)

                logging.info("Saved the best model object in artifacts directory.")

            else:
                logging.info("No best model found with score more than base score")

                raise "No best model found with score more than base score"

        except Exception as e:
            raise SensorException(e, sys) from e
