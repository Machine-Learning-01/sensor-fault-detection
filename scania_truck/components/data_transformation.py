import logging
import os
import sys

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler
from imblearn.combine import SMOTETomek
import pandas as pd
from sklearn.pipeline import Pipeline

from scania_truck.components.data_ingestion import DataIngestion
from scania_truck.exception import ScaniaException
from scania_truck.utils.main_utils import MainUtils
from scania_truck.utils.read_params import read_params

logger = logging.getLogger(__name__)


class DataTransformation:
    def __init__(self):
        self.schema_file = read_params("scania_truck/config/schema.yaml")

        self.data_ingestion = DataIngestion()

        self.utils = MainUtils()

        self.config = read_params()

        self.artifacts_dir = self.config["artifacts_dir"]

        os.makedirs(self.artifacts_dir, exist_ok=True)

    def get_data_transformer_object(self):
        logger.info(
            "Entered get_data_transformer_object method of Data_Ingestion class"
        )

        try:
            logger.info("Got numerical cols from schema config")

            robust_scaler = RobustScaler()

            imputer = SimpleImputer(strategy="constant", fill_value=0)

            logger.info("Initialized RobustScaler, SimpleImputer")

            preprocessor = Pipeline(
                steps=[("Imputer", imputer), ("RobustScaler", robust_scaler)]
            )

            logger.info("Created preprocessor object from ColumnTransformer")

            logger.info(
                "Exited get_data_transformer_object method of Data_Ingestion class"
            )

            return preprocessor

        except Exception as e:
            message = ScaniaException(e, sys)
            raise message.error_message

    def initiate_data_transformation(self, train_set, test_set):
        logger.info(
            "Entered initiate_data_transformation method of Data_Transformation class"
        )

        try:
            preprocessor = self.get_data_transformer_object()

            logger.info("Got the preprocessor object")

            target_column_name = self.schema_file["target_column"]

            logger.info("Got target column name and numerical columns from schema file")

            input_feature_train_df = train_set.drop(
                columns=[target_column_name], axis=1
            )

            target_feature_train_df = train_set[target_column_name]

            target_feature_train_df = target_feature_train_df.replace(
                {"pos": 1, "neg": 0}
            )

            logger.info("Got train features and test features of Training dataset")

            input_feature_test_df = test_set.drop(columns=[target_column_name], axis=1)

            target_feature_test_df = test_set[target_column_name]

            target_feature_test_df = target_feature_test_df.replace(
                {"pos": 1, "neg": 0}
            )

            logger.info("Got train features and test features of Testing dataset")

            logger.info(
                "Applying preprocessing object on training dataframe and testing dataframe"
            )

            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

            logger.info(
                "Used the preprocessor object to fit transform the train features"
            )

            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            logger.info("Used the preprocessor object to transform the test features")

            logger.info("Applying SMOTETomek on Training dataset")

            smt = SMOTETomek(sampling_strategy="minority")

            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df
            )

            logger.info("Applied SMOTETomek on trainng dataset")

            logger.info("Applying SMOTETomek on Testing dataset")

            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df
            )

            logger.info("Applied SMOTETomek on testing dataset")

            logger.info("Created train array and test array")

            train_arr = np.c_[
                input_feature_train_final, np.array(target_feature_train_final)
            ]

            test_arr = np.c_[
                input_feature_test_final, np.array(target_feature_test_final)
            ]

            preprocessor_obj_file_name = (
                self.artifacts_dir + "/" + "scania_truck_preprocessor" + ".pkl"
            )

            self.utils.save_object(preprocessor_obj_file_name, preprocessor)

            logger.info("Saved the preprocessor object")

            logger.info(
                "Exited initiate_data_transformation method of Data_Transformation class"
            )

            return train_arr, test_arr

        except Exception as e:
            message = ScaniaException(e, sys)
            raise message.error_message
