import logging
import sys
from json import loads
from os import environ

import pandas as pd
from pymongo import MongoClient

from scania_truck.exception import ScaniaException

logger = logging.getLogger(__name__)


class MongoDBOperation:
    def __init__(self):
        self.DB_URL = environ["MONGODB_URL"]

        self.client = MongoClient(self.DB_URL)

    def get_database(self, db_name):

        logger.info("Entered get_database method of MongoDB_Operation class")

        try:
            db = self.client[db_name]

            logger.info(f"Created {db_name} database in MongoDB")

            logger.info("Exited get_database method MongoDB_Operation class")

            return db

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def get_collection(self, database, collection_name):

        logger.info("Entered get_collection method of MongoDB_Operation class")

        try:
            collection = database[collection_name]

            logger.info(f"Created {collection_name} collection in mongodb")

            logger.info("Exited get_collection method of MongoDB_Operation class ")

            return collection

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def get_collection_as_dataframe(self, db_name, collection_name):

        logger.info(
            "Entered get_collection_as_dataframe method of MongoDB_Operation class"
        )

        try:
            database = self.get_database(db_name)

            collection = database.get_collection(name=collection_name)

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            logger.info("Converted collection to dataframe")

            logger.info(
                "Exited get_collection_as_dataframe method of MongoDB_Operation class"
            )

            return df

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def insert_dataframe_as_record(self, data_frame, db_name, collection_name):

        logger.info("Entered insert_dataframe_as_record method of MongoDB_Operation")

        try:
            records = loads(data_frame.T.to_json()).values()

            logger.info(f"Converted dataframe to json records")

            database = self.get_database(db_name)

            collection = database.get_collection(collection_name)

            logger.info("Inserting records to MongoDB",)

            collection.insert_many(records)

            logger.info("Inserted records to MongoDB")

            logger.info(
                "Exited the insert_dataframe_as_record method of MongoDB_Operation"
            )

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message
