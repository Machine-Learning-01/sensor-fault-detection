import logging
import sys

import pandas as pd
from pandas import DataFrame

from sensor.cloud_storage.aws_storage import SimpleStorageService
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml_file, MainUtils
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.config_entity import PredictionPipelineConfig


class SensorData:
    def __init__(self, prediction_pipeline_config: PredictionPipelineConfig):
        self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        self.s3 = SimpleStorageService()
        self.prediction_pipeline_config = prediction_pipeline_config

    def get_data(self) -> DataFrame:
        try:
            logging.info("Entered get_data method of SensorData class")
            prediction_df: DataFrame = self.s3.read_csv(filename=self.prediction_pipeline_config.data_file_path,
                                                        bucket_name=self.prediction_pipeline_config.data_bucket_name)
            logging.info("Read prediction csv file from s3 bucket")
            prediction_df = prediction_df.drop(self.schema_config["drop_columns"], axis=1)
            logging.info("Dropped the required columns")
            logging.info("Exited the get_data method of SensorData class")
            return prediction_df
        except Exception as e:
            raise SensorException(e, sys) from e


class SensorClassifier:
    def __init__(self, prediction_pipeline_config: PredictionPipelineConfig):
        self.s3 = SimpleStorageService()
        self.sensor_data = SensorData(prediction_pipeline_config=prediction_pipeline_config)
        self.prediction_pipeline_config = prediction_pipeline_config

    def predict(self) -> None:
        logging.info("Entered predict method of CarPricePredictor class")

        try:
            input_dataframe = self.sensor_data.get_data()

            model = self.s3.load_model(self.prediction_pipeline_config.model_file_path,
                                       self.prediction_pipeline_config.model_bucket_name, )
            logging.info("Loaded best model from s3 bucket")
            result = list(model.predict(input_dataframe))
            result = DataFrame(list((result)), columns=["Prediction"])
            result = pd.concat([input_dataframe,result],axis=1)
            self.s3.upload_df_as_csv(
                result,
                self.prediction_pipeline_config.output_file_name,
                self.prediction_pipeline_config.output_file_name,
                self.prediction_pipeline_config.data_bucket_name,
            )

            logging.info(
                "Used best model to get predictions and prediction are stored in io files bucket"
            )
            logging.info("Exited predict method of CarPricePredictor class")
        except Exception as e:
            raise SensorException(e, sys) from e
