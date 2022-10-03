import logging
import shutil
import sys

import dill
import xgboost
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import all_estimators
from yaml import safe_dump

from sensor.cloud_storage.s3_operations import S3Operation
from sensor.exception import SensorException
from sensor.utils.read_params import read_params

logger = logging.getLogger(__name__)

config_ = "Sensor_truck/config/params.yaml"


class MainUtils:
    def __init__(self):
        self.s3 = S3Operation()

        self.config = read_params()

        self.tuner_kwargs = self.config["model_utils"]

        self.artifacts_dir = self.config["artifacts_dir"]

        self.io_files_bucket = self.config["s3_bucket"][
            "Sensor_truck_input_files_bucket"
        ]

    def get_tuned_model(self, model_name, train_x, train_y, test_x, test_y):
        try:
            self.model = self.get_base_model(model_name)

            self.model_best_params = self.get_model_params(self.model, train_x, train_y)

            self.model.set_params(**self.model_best_params)

            self.model.fit(train_x, train_y)

            self.preds = self.model.predict(test_x)

            self.model_score = self.get_model_score(test_y, self.preds)

            return self.model_score, self.model, self.model.__class__.__name__

        except Exception as e:
            raise e

    def get_model_score(self, test_y, preds):
        try:
            self.model_score = r2_score(test_y, preds)

            return self.model_score

        except Exception as e:
            message = SensorException(e, sys)
            raise message.error_message

    def get_base_model(self, model_name):
        try:
            if model_name.lower().startswith("xgb") is True:
                model = xgboost.__dict__[model_name]()

            else:
                model_idx = [model[0] for model in all_estimators()].index(model_name)

                model = all_estimators().__getitem__(model_idx)[1]()

            return model

        except Exception as e:
            raise e

    def get_model_params(self, model, x_train, y_train):
        try:
            model_name = model.__class__.__name__

            self.model_param_grid = self.config["train_model"][model_name]

            self.model_grid = GridSearchCV(
                model, self.model_param_grid, **self.tuner_kwargs
            )

            self.model_grid.fit(x_train, y_train)

            return self.model_grid.best_params_

        except Exception as e:
            raise e

    @staticmethod
    def save_object(file_path, obj):
        try:
            with open(file_path, "wb") as file_obj:
                dill.dump(obj, file_obj)

        except Exception as e:
            raise e

    @staticmethod
    def get_best_model_with_name_and_score(lst):
        try:
            best_score = max(lst)[0]

            best_model = max(lst)[1]

            return best_model, best_score

        except Exception as e:
            raise e

    @staticmethod
    def load_object(file_path):
        try:
            with open(file_path, "rb") as file_obj:
                return dill.load(file_obj)

        except Exception as e:
            raise e

    @staticmethod
    def create_artifacts_zip(file_name, folder_name):
        try:
            shutil.make_archive(file_name, "zip", folder_name)

        except Exception as e:
            raise e

    @staticmethod
    def unzip_file(filename, folder_name):
        try:
            shutil.unpack_archive(filename, folder_name)

        except Exception as e:
            raise e

    def update_model_score(self, best_model_score):
        try:

            self.config["base_model_score"] = str(best_model_score)

            with open(config_, "w+") as fp:
                safe_dump(self.config, fp, sort_keys=False)

        except Exception as e:
            raise e
