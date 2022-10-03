import logging
import shutil
import sys

import dill
import xgboost
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import all_estimators
from yaml import safe_dump

from sensor.cloud_storage.s3_operations import S3Operation
from sensor.exception import SensorException
from sensor.utils.read_params import read_params

logger = logging.getLogger(__name__)

config_ = "sensor/config/params.yaml"


class MainUtils:
    def __init__(self):
        self.s3 = S3Operation()

        self.config = read_params()

        self.tuner_kwargs = self.config["model_utils"]

        self.artifacts_dir = self.config["artifacts_dir"]

        self.io_files_bucket = self.config["s3_bucket"]["sensor_input_files_bucket"]

    def get_tuned_model(self, model_name, train_x, train_y, test_x, test_y):
        logger.info("Entered the get_tuned_model method of MainUtils class")

        try:
            self.model = self.get_base_model(model_name)

            self.model_best_params = self.get_model_params(self.model, train_x, train_y)

            self.model.set_params(**self.model_best_params)

            self.model.fit(train_x, train_y)

            self.preds = self.model.predict(test_x)

            self.model_score = self.get_model_score(test_y, self.preds)

            logger.info("Entered the get_tuned_model method of MainUtils class")

            return self.model_score, self.model, self.model.__class__.__name__

        except Exception as e:
            raise SensorException(e, sys) from e

    def get_model_score(self, test_y, preds):
        logger.info("Entered the get_model_score method of MainUtils class")

        try:
            self.model_score = roc_auc_score(test_y, preds)

            logger.info("Model score is {}".format(self.model_score))

            logger.info("Exited the get_model_score method of MainUtils class")

            return self.model_score

        except Exception as e:
            raise SensorException(e, sys) from e

    def get_base_model(self, model_name):
        logger.info("Entered the get_base_model method of MainUtils class")

        try:
            if model_name.lower().startswith("xgb") is True:
                model = xgboost.__dict__[model_name]()

            else:
                model_idx = [model[0] for model in all_estimators()].index(model_name)

                model = all_estimators().__getitem__(model_idx)[1]()

            logger.info("Exited the get_base_model method of MainUtils class")

            return model

        except Exception as e:
            raise SensorException(e, sys) from e

    def get_model_params(self, model, x_train, y_train):
        logger.info("Entered the get_model_params method of MainUtils class")

        try:
            model_name = model.__class__.__name__

            self.model_param_grid = self.config["train_model"][model_name]

            self.model_grid = GridSearchCV(
                model, self.model_param_grid, **self.tuner_kwargs
            )

            self.model_grid.fit(x_train, y_train)

            logger.info("Exited the get_model_params method of MainUtils class")

            return self.model_grid.best_params_

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def save_object(file_path, obj):
        logger.info("Entered the save_object method of MainUtils class")

        try:
            with open(file_path, "wb") as file_obj:
                dill.dump(obj, file_obj)

            logger.info("Exited the save_object method of MainUtils class")

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def get_best_model_with_name_and_score(lst):
        logger.info(
            "Entered the get_best_model_with_name_and_score method of MainUtils class"
        )

        try:
            best_score = max(lst)[0]

            best_model = max(lst)[1]

            logger.info(
                "Exited the get_best_model_with_name_and_score method of MainUtils class"
            )

            return best_model, best_score

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def load_object(file_path):
        logger.info("Entered the load_object method of MainUtils class")

        try:
            with open(file_path, "rb") as file_obj:
                obj = dill.load(file_obj)

            logger.info("Exited the load_object method of MainUtils class")

            return obj

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def create_artifacts_zip(file_name, folder_name):
        logger.info("Entered the create_artifacts_zip method of MainUtils class")

        try:
            shutil.make_archive(file_name, "zip", folder_name)

            logger.info("Exited the create_artifacts_zip method of MainUtils class")

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def unzip_file(filename, folder_name):
        logger.info("Entered the unzip_file method of MainUtils class")

        try:
            shutil.unpack_archive(filename, folder_name)

            logger.info("Exited the unzip_file method of MainUtils class")

        except Exception as e:
            raise SensorException(e, sys) from e

    def update_model_score(self, best_model_score):
        logger.info("Entered the update_model_score method of MainUtils class")

        try:

            self.config["base_model_score"] = str(best_model_score)

            with open(config_, "w+") as fp:
                safe_dump(self.config, fp, sort_keys=False)

            logger.info("Exited the update_model_score method of MainUtils class")

        except Exception as e:
            raise SensorException(e, sys) from e
