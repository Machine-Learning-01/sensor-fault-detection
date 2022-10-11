import os.path
import shutil
import sys
from typing import Dict, Tuple
import numpy as np
import dill
import xgboost
import yaml
from pandas import DataFrame
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import all_estimators
from yaml import safe_dump

from sensor.constant.training_pipeline import MODEL_TRAINER_MODEL_CONFIG_FILE_PATH, SCHEMA_FILE_PATH
from sensor.entity.config_entity import TunerConfig
from sensor.exception import SensorException
from sensor.logger import logging


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise SensorException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise SensorException(e, sys)


def load_object(file_path: str) -> object:
    logging.info("Entered the load_object method of MainUtils class")

    try:

        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)

        logging.info("Exited the load_object method of MainUtils class")

        return obj

    except Exception as e:
        raise SensorException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise SensorException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    logging.info("Entered the save_object method of MainUtils class")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info("Exited the save_object method of MainUtils class")

    except Exception as e:
        raise SensorException(e, sys) from e


class MainUtils:
    def __init__(self) -> None:
        self.tuner_config = TunerConfig()

    def read_yaml_file(self, filename: str) -> dict:
        try:
            with open(filename, "rb") as yaml_file:
                return yaml.safe_load(yaml_file)

        except Exception as e:
            raise SensorException(e, sys) from e

    def read_schema_config_file(self) -> dict:
        try:
            schema_config = self.read_yaml_file(SCHEMA_CONFIG_FILE)

            return schema_config

        except Exception as e:
            raise SensorException(e, sys) from e

    def read_model_config_file(self) -> dict:
        try:
            model_config = self.read_yaml_file(MODEL_CONFIG_FILE)

            return model_config

        except Exception as e:
            raise SensorException(e, sys) from e

    def get_tuned_model(
            self,
            model_name: str,
            train_x: DataFrame,
            train_y: DataFrame,
            test_x: DataFrame,
            test_y: DataFrame,
    ) -> Tuple[float, object, str]:

        logging.info("Entered the get_tuned_model method of MainUtils class")

        try:
            model = self.get_base_model(model_name)

            model_best_params = self.get_model_params(model, train_x, train_y)

            model.set_params(**model_best_params)

            model.fit(train_x, train_y)

            preds = model.predict(test_x)

            model_score = self.get_model_score(test_y, preds)

            logging.info("Entered the get_tuned_model method of MainUtils class")

            return model_score, model, model.__class__.__name__

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def get_model_score(test_y: DataFrame, preds: DataFrame) -> float:
        logging.info("Entered the get_model_score method of MainUtils class")

        try:
            model_score = roc_auc_score(test_y, preds)

            logging.info("Model score is {}".format(model_score))

            logging.info("Exited the get_model_score method of MainUtils class")

            return model_score

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def get_base_model(model_name: str) -> object:
        logging.info("Entered the get_base_model method of MainUtils class")

        try:
            if model_name.lower().startswith("xgb") is True:
                model = xgboost.__dict__[model_name]()

            else:
                model_idx = [model[0] for model in all_estimators()].index(model_name)

                model = all_estimators().__getitem__(model_idx)[1]()

            logging.info("Exited the get_base_model method of MainUtils class")

            return model

        except Exception as e:
            raise SensorException(e, sys) from e

    def get_model_params(
            self, model: object, x_train: DataFrame, y_train: DataFrame
    ) -> Dict:
        logging.info("Entered the get_model_params method of MainUtils class")

        try:
            model_name = model.__class__.__name__

            model_config = self.read_model_config_file()

            model_param_grid = model_config["train_model"][model_name]

            model_grid = GridSearchCV(
                model, model_param_grid, **self.tuner_config.__dict__
            )

            model_grid.fit(x_train, y_train)

            logging.info("Exited the get_model_params method of MainUtils class")

            return model_grid.best_params_

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def save_object(file_path: str, obj: object) -> None:
        logging.info("Entered the save_object method of MainUtils class")

        try:
            with open(file_path, "wb") as file_obj:
                dill.dump(obj, file_obj)

            logging.info("Exited the save_object method of MainUtils class")

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def get_best_model_with_name_and_score(model_list: list) -> Tuple[object, float]:
        logging.info(
            "Entered the get_best_model_with_name_and_score method of MainUtils class"
        )

        try:
            best_score = max(model_list)[0]

            best_model = max(model_list)[1]

            logging.info(
                "Exited the get_best_model_with_name_and_score method of MainUtils class"
            )

            return best_model, best_score

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def load_object(file_path: str) -> object:
        logging.info("Entered the load_object method of MainUtils class")

        try:
            with open(file_path, "rb") as file_obj:
                obj = dill.load(file_obj)

            logging.info("Exited the load_object method of MainUtils class")

            return obj

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def create_artifacts_zip(file_name: str, folder_name: str) -> None:
        logging.info("Entered the create_artifacts_zip method of MainUtils class")

        try:
            shutil.make_archive(file_name, "zip", folder_name)

            logging.info("Exited the create_artifacts_zip method of MainUtils class")

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def unzip_file(filename: str, folder_name: str) -> None:
        logging.info("Entered the unzip_file method of MainUtils class")

        try:
            shutil.unpack_archive(filename, folder_name)

            logging.info("Exited the unzip_file method of MainUtils class")

        except Exception as e:
            raise SensorException(e, sys) from e

    def update_model_score(self, best_model_score: float) -> None:
        logging.info("Entered the update_model_score method of MainUtils class")

        try:
            model_config = self.read_model_config_file()

            model_config["base_model_score"] = str(best_model_score)

            with open(MODEL_CONFIG_FILE, "w+") as fp:
                safe_dump(model_config, fp, sort_keys=False)

            logging.info("Exited the update_model_score method of MainUtils class")

        except Exception as e:
            raise SensorException(e, sys) from e
