import logging
import sys

from sensor.cloud_storage.s3_operations import S3Operation
from sensor.exception import SensorException
from sensor.utils.main_utils import MainUtils
from sensor.utils.read_params import read_params

logger = logging.getLogger(__name__)


class SensorModel:
    def __init__(self, preprocessing_object, trained_model_object):

        self.preprocessing_object = preprocessing_object

        self.trained_model_object = trained_model_object

    def predict(self, X):
        logger.info("Entered predict method of SensorTruckModel class")

        try:
            logger.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(X)

            logger.info("Used the trained model to get predictions")

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

        self.config = read_params()

        self.artifacts_dir = self.config["artifacts_dir"]

        self.io_files_bucket = self.config["s3_bucket"]["sensor_input_files_bucket"]

        self.preprocessor_obj_file_name = self.config["preprocessor_obj_file_name"]

    def get_trained_models(self, X_data, Y_data):

        logger.info("Entered the get_trained_models method of ModelFinder class")

        try:
            models_list = list(self.config["train_model"].keys())

            logger.info("Got model list from the config file")

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

            logger.info("Got trained model list")

            logger.info("Exited the get_trained_models method of ModelFinder class")

            return tuned_model_list

        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_model_trainer(self, train_set, test_set):
        logger.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:            
            list_of_trained_models = self.get_trained_models(train_set,test_set)

            logger.info("Got a list of tuple of model score, model and model name")

            (
                best_model,
                best_model_score,
            ) = self.utils.get_best_model_with_name_and_score(list_of_trained_models)

            logger.info("Got best model score, model and model name")

            preprocessing_obj = self.utils.load_object(self.preprocessor_obj_file_name)

            logger.info("Loaded preprocessing object")

            base_model_score = float(self.config["base_model_score"])

            if best_model_score >= base_model_score:

                self.utils.update_model_score(best_model_score)

                logger.info("Updating model score in yaml file")

                sensor_model = SensorModel(
                    preprocessing_object=preprocessing_obj,
                    trained_model_object=best_model,
                )

                logger.info(
                    "Created Sensor truck model object with preprocessor and model"
                )

                best_model_file_path = self.artifacts_dir + "/" + "model" + ".sav"

                logger.info("Created best model file path.")

                self.utils.save_object(best_model_file_path, sensor_model)

                logger.info("Saved the best model object in artifacts directory.")

            else:
                logger.info("No best model found with score more than base score")

                raise "No best model found with score more than base score"

        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_model_pusher(self):
        logger.info("Entered initiate_model_pusher method of ModelTrainer class")

        try:
            logger.info("Uploading artifacts folder to s3 bucket")

            self.s3.upload_folder(self.artifacts_dir, self.io_files_bucket)

            logger.info("Uploaded artifacts folder to s3 bucket")

            logger.info("Exited initiate_model_pusher method of ModelTrainer class")

        except Exception as e:
            raise SensorException(e, sys) from e
