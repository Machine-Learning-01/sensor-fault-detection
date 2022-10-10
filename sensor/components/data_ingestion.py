import sys
from typing import Tuple

import numpy as np
from pandas import DataFrame
from sklearn.model_selection import train_test_split

from sensor.configuration.mongo_client import MongoDBOperation
from sensor.entity.config_entity import DataIngestionConfig,DatabaseConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import MainUtils
from sensor.data_access.sensor_data import SensorData
from typing import List
import os
from sensor.logger import logging
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        """

        """
        try:
            self.data_ingestion_config = data_ingestion_config
            # self.utils = MainUtils()

            # self.mongo_op = MongoDBOperation()

            # self.mongo_config = DatabaseConfig()
        except Exception as e:
            raise SensorException(e,sys)

    def export_data_into_feature_store(self)->DataFrame:
        try:
            logging.info(f"Exporting data from mongodb")
            sensor_data = SensorData()
            dataframe = sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            feature_store_file_path  = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise SensorException(e,sys)



    def split_data_as_train_test(self,dataframe: DataFrame) ->List[str]:
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
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
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
                self.mongo_config.DATABASE_NAME, self.mongo_config.COLLECTION_NAME
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
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
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
