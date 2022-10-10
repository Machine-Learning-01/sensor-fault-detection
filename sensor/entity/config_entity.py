import os
from sensor.constant.training_pipeline import *
from pymongo import MongoClient
from dataclasses import dataclass
from datetime import datetime

TIMESTAMP:str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig:
    pipeline_name:str = PIPELINE_NAME
    artifact_dir:str = os.path.join(ARTIFACT_DIR,TIMESTAMP)
    timestamp:str = TIMESTAMP
    

training_pipeline_config:TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir:str = os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
    feature_store_file_path:str  = os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)
    training_file_path:str = os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TRAIN_FILE_NAME)
    testing_file_path:str = os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TEST_FILE_NAME)
    train_test_split_ratio:float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATION 
@dataclass
class DataValidationConfig:
    data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir,DATA_VALIDATION_DIR_NAME)
    valid_data_dir:str = os.path.join(data_validation_dir,DATA_VALIDATION_VALID_DIR)
    invalid_data_dir:str = os.path.join(data_validation_dir,DATA_VALIDATION_INVALID_DIR)
    valid_train_file_path:str = os.path.join(valid_data_dir,TRAIN_FILE_NAME)
    valid_test_file_path:str = os.path.join(valid_data_dir,TEST_FILE_NAME)
    invalid_train_file_path:str = os.path.join(invalid_data_dir,TRAIN_FILE_NAME)
    invalid_test_file_path:str = os.path.join(invalid_data_dir,TEST_FILE_NAME)
    

@dataclass
class DataTransformationConfig:
    data_transformation_dir:str = os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR_NAME)
    transformed_train_file_path:str=os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,TRAIN_FILE_NAME)
    transformed_test_file_path:str = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,TEST_FILE_NAME)
    transformed_object_file_path:str = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,PREPROCSSING_OBJECT_FILE_NAME )

@dataclass
class ModelTrainerConfig:
    model_trainer_dir:str = os.path.join(training_pipeline_config.artifact_dir,MODEL_TRAINER_DIR_NAME)
    trained_model_file_path:str = os.path.join(model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR,MODEL_FILE_NAME )
    expected_accuracy:float = MODEL_TRAINER_EXPECTED_SCORE
    
@dataclass
class ModelEvaluationConfig:
    changed_threshold_score:float = MODEL_EVALUATION_CHANGED_THREASHOLD_SCORE

@dataclass
class ModelPusherConfig:
    bucket_name:str =  MODEL_PUSHER_BUCKET_NAME
    s3_model_key_path:str = os.pa.path.join(MODEL_PUSHER_BUCKET_NAME,MODEL_PUSHER_S3_KEY,MODEL_FILE_NAME)








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

    def get_database_config(self):
        return self.__dict__


class SimpleImputerConfig:
    def __init__(self):
        self.strategy = "constant"

        self.fill_value = 0

    def get_simple_imputer_config(self):
        return self.__dict__
