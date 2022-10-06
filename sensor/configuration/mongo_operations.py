import sys
from json import loads

from pandas import DataFrame
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from sensor.entity.config_entity import DatabaseConfig
from sensor.exception import SensorException
from sensor.logger import logging


class MongoDBOperation:
    def __init__(self):
        self.mongo_config = DatabaseConfig()

        self.client = MongoClient(self.mongo_config.DB_URL)

    def get_database(self, database_name: str) -> Database:

        logging.info("Entered get_database method of MongoDB_Operation class")

        try:
            db = self.client[database_name]

            logging.info(f"Created {database_name} database in MongoDB")

            logging.info("Exited get_database method MongoDB_Operation class")

            return db

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def get_collection(database: Database, collection_name: str) -> Collection:

        logging.info("Entered get_collection method of MongoDB_Operation class")

        try:
            collection = database[collection_name]

            logging.info(f"Created {collection_name} collection in mongodb")

            logging.info("Exited get_collection method of MongoDB_Operation class ")

            return collection

        except Exception as e:
            raise SensorException(e, sys) from e

    def get_collection_as_dataframe(
        self, database_name: str, collection_name: str
    ) -> DataFrame:
        logging.info(
            "Entered get_collection_as_dataframe method of MongoDB_Operation class"
        )

        try:
            database = self.get_database(database_name)

            logging.info("Getting collection from database")

            collection = database.get_collection(name=collection_name)

            logging.info("Got a collection from database")

            df = DataFrame(list(collection.find()))

            logging.info("Created a dataframe from the collection")

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            logging.info("Converted collection to dataframe")

            logging.info(
                "Exited get_collection_as_dataframe method of MongoDB_Operation class"
            )

            return df

        except Exception as e:
            raise SensorException(e, sys) from e

    def insert_dataframe_as_record(
        self, data_frame: DataFrame, database_name: str, collection_name: str
    ) -> None:

        logging.info("Entered insert_dataframe_as_record method of MongoDB_Operation")

        try:
            records = loads(data_frame.T.to_json()).values()

            logging.info(f"Converted dataframe to json records")

            database = self.get_database(database_name)

            collection = database.get_collection(collection_name)

            logging.info("Inserting records to MongoDB",)

            collection.insert_many(records)

            logging.info("Inserted records to MongoDB")

            logging.info(
                "Exited the insert_dataframe_as_record method of MongoDB_Operation"
            )

        except Exception as e:
            raise SensorException(e, sys) from e
