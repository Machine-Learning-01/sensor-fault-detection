import sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
from sensor.entity.config_entity import DataTransformationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.ml.model.estimator import TargetValueMapping
from sensor.utils.main_utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        """

        :param data_validation_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_validation_artifact

            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise SensorException(e, sys)

    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        """
        :return: Pipeline object to transform dataset
        """
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )

        try:
            logging.info("Got numerical cols from schema config")

            robust_scaler = RobustScaler()

            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)

            logging.info("Initialized RobustScaler, Simple Imputer")

            preprocessor = Pipeline(
                steps=[("Imputer", simple_imputer), ("RobustScaler", robust_scaler)]
            )

            logging.info("Created preprocessor object from ColumnTransformer")

            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )

            return preprocessor

        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_data_transformation(self,) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")

            preprocessor = self.get_data_transformer_object()

            logging.info("Got the preprocessor object")

            train_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path
            )

            test_df = DataTransformation.read_data(
                file_path=self.data_validation_artifact.valid_test_file_path
            )

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_train_df = train_df[TARGET_COLUMN]

            target_feature_train_df = target_feature_train_df.replace(
                TargetValueMapping().to_dict()
            )

            logging.info("Got train features and test features of Training dataset")

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_test_df = test_df[TARGET_COLUMN]

            target_feature_test_df = target_feature_test_df.replace(
                TargetValueMapping().to_dict()
            )

            logging.info("Got train features and test features of Testing dataset")

            logging.info(
                "Applying preprocessing object on training dataframe and testing dataframe"
            )

            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

            logging.info(
                "Used the preprocessor object to fit transform the train features"
            )

            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            logging.info("Used the preprocessor object to transform the test features")

            logging.info("Applying SMOTETomek on Training dataset")

            smt = SMOTETomek(sampling_strategy="minority")

            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df
            )

            logging.info("Applied SMOTETomek on training dataset")

            logging.info("Applying SMOTETomek on testing dataset")

            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df
            )

            logging.info("Applied SMOTETomek on testing dataset")

            logging.info("Created train array and test array")

            train_arr = np.c_[
                input_feature_train_final, np.array(target_feature_train_final)
            ]

            test_arr = np.c_[
                input_feature_test_final, np.array(target_feature_test_final)
            ]

            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor,
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr,
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr,
            )

            logging.info("Saved the preprocessor object")

            logging.info(
                "Exited initiate_data_transformation method of Data_Transformation class"
            )

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys) from e
