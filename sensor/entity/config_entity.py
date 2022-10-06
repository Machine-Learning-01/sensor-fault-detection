import os

from pymongo import MongoClient


class S3Config:
    def __init__(self):
        self.IO_FILES_BUCKET = "sensor-io-files"

        self.PRED_DATA_BUCKET = "sensor-pred-data"

    def get_s3_config(self):
        return self.__dict__


class TunerConfig:
    def __init__(self):
        self.verbose = 2

        self.cv = 2

        self.n_jobs = -1

    def get_tuner_config(self):
        return self.__dict__


class DatabaseConfig:
    def __init__(self):
        self.DATABASE_NAME = "ineuron"

        self.COLLECTION_NAME = "sensor"

        self.DB_URL = os.environ["MONGODB_URL"]

        self.mongo_client = MongoClient(self.DB_URL)

    def get_database_config(self):
        return self.__dict__


class SimpleImputerConfig:
    def __init__(self):
        self.strategy = "constant"

        self.fill_value = 0

    def get_simple_imputer_config(self):
        return self.__dict__
