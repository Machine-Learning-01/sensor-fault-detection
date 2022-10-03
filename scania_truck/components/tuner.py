import logging
import sys

from scania_truck.exception import ScaniaException
from scania_truck.utils.main_utils import MainUtils
from scania_truck.utils.read_params import read_params


logger = logging.getLogger(__name__)


class ModelFinder:
    def __init__(self):
        self.config = read_params()

        self.utils = MainUtils()

    def get_trained_models(self, X_data, Y_data):
        try:
            models_list = list(self.config["train_model"].keys())

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

            return tuned_model_list

        except Exception as e:
            message = ScaniaException(e, sys)
            raise message.error_message
