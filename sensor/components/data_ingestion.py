import sys
from typing import Tuple

import numpy as np
from pandas import DataFrame
from sklearn.model_selection import train_test_split

from sensor.configuration.config import MongoDBOperation
from sensor.constant import TRAIN_TEST_SPLIT_SIZE
from sensor.entity.config_entity import DatabaseConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import MainUtils


class DataIngestion:
    def __init__(self):
        self.utils = MainUtils()

        self.mongo_op = MongoDBOperation()

        self.mongo_config = DatabaseConfig()

    @staticmethod
    def split_data_as_train_test(df: DataFrame) -> Tuple(DataFrame, DataFrame):
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            train_set, test_set = train_test_split(df, test_size=TRAIN_TEST_SPLIT_SIZE)

            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )

            return train_set, test_set

        except Exception as e:
            raise SensorException(e, sys) from e

    def get_data_from_mongodb(self) -> DataFrame:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered get_data_from_mongodb method of Data_Ingestion class")

        try:
            logging.info("Getting the dataframe from mongodb")

            df = self.mongo_op.get_collection_as_dataframe(
                self.mongo_config.database_name, self.mongo_config.collection_name
            )

            df = df.replace("na", np.nan)

            logging.info("Got the dataframe from mongodb")

            logging.info(
                "Exited the get_data_from_mongodb method of Data_Ingestion class"
            )

            return df

        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_data_ingestion(self) -> Tuple[DataFrame, DataFrame]:
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            df = self.get_data_from_mongodb()

            _schema_config = self.utils.read_schema_config_file()

            df1 = df.drop(_schema_config["drop_columns"], axis=1)

            logging.info("Got the data from mongodb")

            train_set, test_set = self.split_data_as_train_test(df1)

            logging.info("Performed train test split on the dataset")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )

            return train_set, test_set

        except Exception as e:
            raise SensorException(e, sys) from e
