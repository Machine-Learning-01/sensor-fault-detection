import sys

import numpy as np
import pandas as pd
from pandas import DataFrame

from sensor.cloud_storage.aws_storage import SimpleStorageService
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.config_entity import PredictionPipelineConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.ml.model.estimator import TargetValueMapping
from sensor.ml.model.s3_estimator import SensorEstimator
from sensor.utils.main_utils import read_yaml_file


class PredictionPipeline:
    def __init__(
        self,
        prediction_pipeline_config: PredictionPipelineConfig = PredictionPipelineConfig(),
    ) -> None:
        """
        :param prediction_pipeline_config:
        """
        try:
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)

            self.prediction_pipeline_config = prediction_pipeline_config

            self.s3 = SimpleStorageService()

        except Exception as e:
            raise SensorException(e, sys)

    def get_data(self) -> DataFrame:
        try:
            logging.info("Entered get_data method of SensorData class")

            prediction_df = self.s3.read_csv(
                filename=self.prediction_pipeline_config.data_file_path,
                bucket_name=self.prediction_pipeline_config.data_bucket_name,
            )

            logging.info("Read prediction csv file from s3 bucket")

            prediction_df = prediction_df.drop(
                self.schema_config["drop_columns"], axis=1
            )

            logging.info("Dropped the required columns")

            logging.info("Exited the get_data method of SensorData class")

            return prediction_df

        except Exception as e:
            raise SensorException(e, sys)

    def predict(self, dataframe) -> np.ndarray:
        try:
            logging.info("Entered predict method of SensorData class")

            model = SensorEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )

            return model.predict(dataframe)

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_prediction(self,) -> None:
        try:
            dataframe = self.get_data()

            predicted_arr = self.predict(dataframe)

            prediction = pd.DataFrame(list(predicted_arr))

            prediction.columns = ["class"]

            prediction.replace(TargetValueMapping().reverse_mapping(), inplace=True)

            predicted_dataframe = pd.concat([dataframe, prediction], axis=1)

            self.s3.upload_df_as_csv(
                predicted_dataframe,
                self.prediction_pipeline_config.output_file_name,
                self.prediction_pipeline_config.output_file_name,
                self.prediction_pipeline_config.data_bucket_name,
            )

            logging.info("Uploaded artifacts folder to s3 bucket_name")

            logging.info(f"File has uploaded to {predicted_dataframe}")

        except Exception as e:
            raise SensorException(e, sys)
