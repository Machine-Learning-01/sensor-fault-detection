import sys
from typing import Union

import numpy as np
from imblearn.combine import SMOTETomek
from pandas import DataFrame
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from sensor.components.data_ingestion import DataIngestion
from sensor.constant import PREPROCESSOR_OBJ_FILE_NAME, TARGET_COLUMN
from sensor.entity.config_entity import SimpleImputerConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import MainUtils


class DataTransformation:
    def __init__(self):
        self.data_ingestion = DataIngestion()

        self.imputer_config = SimpleImputerConfig()

        self.utils = MainUtils()

    def get_data_transformer_object(self) -> object:
        """
        Method Name :   get_data_transformer_object
        Description :   This method creates and returns a data transformer object 
        
        Output      :   data transformer object is created and returned 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )

        try:
            logging.info("Got numerical cols from schema config")

            robust_scaler = RobustScaler()

            imputer = SimpleImputer(**self.imputer_config.__dict__)

            logging.info("Initialized RobustScaler, SimpleImputer")

            preprocessor = Pipeline(
                steps=[("Imputer", imputer), ("RobustScaler", robust_scaler)]
            )

            logging.info("Created preprocessor object from ColumnTransformer")

            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )

            return preprocessor

        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_data_transformation(
        self, train_set: DataFrame, test_set: DataFrame
    ) -> Union[np.ndarray, np.ndarray]:
        """
        Method Name :   initiate_data_transformation
        Description :   This method initiates the data transformation component for the pipeline 
        
        Output      :   data transformer object is created and returned 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info(
            "Entered initiate_data_transformation method of Data_Transformation class"
        )

        try:
            preprocessor = self.get_data_transformer_object()

            logging.info("Got the preprocessor object")

            input_feature_train_df = train_set.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_train_df = train_set[TARGET_COLUMN]

            target_feature_train_df = target_feature_train_df.replace(
                {"pos": 1, "neg": 0}
            )

            logging.info("Got train features and test features of Training dataset")

            input_feature_test_df = test_set.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_test_df = test_set[TARGET_COLUMN]

            target_feature_test_df = target_feature_test_df.replace(
                {"pos": 1, "neg": 0}
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

            self.utils.save_object(PREPROCESSOR_OBJ_FILE_NAME, preprocessor)

            logging.info("Saved the preprocessor object")

            logging.info(
                "Exited initiate_data_transformation method of Data_Transformation class"
            )

            return train_arr, test_arr

        except Exception as e:
            raise SensorException(e, sys) from e
