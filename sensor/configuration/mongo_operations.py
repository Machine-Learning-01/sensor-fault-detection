import sys
from json import loads
from os import environ

import pandas as pd
from pymongo import MongoClient

from sensor.exception import SensorException
from sensor.logger import logging


class MongoDBOperation:
    def __init__(self):
        self.DB_URL = environ["MONGODB_URL"]

        self.client = MongoClient(self.DB_URL)

    def get_database(self, db_name):

        logging.info("Entered get_database method of MongoDB_Operation class")

        try:
            db = self.client[db_name]

            logging.info(f"Created {db_name} database in MongoDB")

            logging.info("Exited get_database method MongoDB_Operation class")

            return db

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def get_collection(database, collection_name):

        logging.info("Entered get_collection method of MongoDB_Operation class")

        try:
            collection = database[collection_name]

            logging.info(f"Created {collection_name} collection in mongodb")

            logging.info("Exited get_collection method of MongoDB_Operation class ")

            return collection

        except Exception as e:
            raise SensorException(e, sys) from e

    def get_collection_as_dataframe(self, db_name, collection_name):

        logging.info(
            "Entered get_collection_as_dataframe method of MongoDB_Operation class"
        )

        try:
            database = self.get_database(db_name)

            collection = database.get_collection(name=collection_name)

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            logging.info("Converted collection to dataframe")

            logging.info(
                "Exited get_collection_as_dataframe method of MongoDB_Operation class"
            )

            return df

        except Exception as e:
            raise SensorException(e, sys) from e

    def insert_dataframe_as_record(self, data_frame, db_name, collection_name):

        logging.info("Entered insert_dataframe_as_record method of MongoDB_Operation")

        try:
            records = loads(data_frame.T.to_json()).values()

            logging.info(f"Converted dataframe to json records")

            database = self.get_database(db_name)

            collection = database.get_collection(collection_name)

            logging.info("Inserting records to MongoDB",)

            collection.insert_many(records)

            logging.info("Inserted records to MongoDB")

            logging.info(
                "Exited the insert_dataframe_as_record method of MongoDB_Operation"
            )

        except Exception as e:
            raise SensorException(e, sys) from e
