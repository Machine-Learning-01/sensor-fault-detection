import logging
import sys
import numpy as np
from sklearn.model_selection import train_test_split
from scania_truck.cloud_storage.s3_operations import S3Operation

from scania_truck.exception import ScaniaException
from scania_truck.utils.mongo_operations import MongoDBOperation
from scania_truck.utils.read_params import read_params

logger = logging.getLogger(__name__)

mongo_op = MongoDBOperation()


class DataIngestion:
    def __init__(self):
        self.config = read_params()
<<<<<<< HEAD

        self.schema_config = read_params("scania_truck/config/schema.yaml")
=======
        self.s3 = S3Operation()
        self.schema_file = read_params("scania_truck/config/schema.yaml")
>>>>>>> 6d9d288ae9fd9109ec38541389d30357ae55a309

        self.db_name = self.config["mongo"]["db_name"]

        self.collection_name = self.config["mongo"]["collection_name"]

        self.drop_cols = self.schema_config["drop_columns"]

    @staticmethod
    def split_data_as_train_test(df):
        logger.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            train_set, test_set = train_test_split(df, test_size=0.2)

            logger.info("Performed train test split on the dataframe")

            logger.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )

            return train_set, test_set

        except Exception as e:

            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def get_data_from_mongodb(self):
        logger.info("Entered get_data_from_mongodb method of Data_Ingestion class")

        try:
            logger.info("Getting the dataframe from mongodb")

            df = mongo_op.get_collection_as_dataframe(
                self.db_name, self.collection_name
            )

            df = df.replace("na", np.nan)

            logger.info("Got the dataframe from mongodb")

            logger.info(
                "Exited the get_data_from_mongodb method of Data_Ingestion class"
            )

            return df

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def initiate_data_ingestion(self):
        logger.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            df = self.get_data_from_mongodb()

            df1 = df.drop(self.drop_cols, axis=1)

            logger.info("Got the data from mongodb")

            train_set, test_set = self.split_data_as_train_test(df1)

            logger.info("Performed train test split on the dataset")

            logger.info("Exited initiate_data_ingestion method of Data_Ingestion class")

            return train_set, test_set

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message
