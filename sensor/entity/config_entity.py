import os
from dataclasses import dataclass
from datetime import datetime

from sensor.constant import prediction_pipeline
from sensor.constant.training_pipeline import *
from sensor.entity.artifact_entity import ClassificationMetricArtifact

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME

    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)

    timestamp: str = TIMESTAMP


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME
    )

    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME
    )

    training_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME
    )

    testing_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME
    )

    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATION

    collection_name: str = DATA_INGESTION_COLLECTION_NAME


@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME
    )

    valid_data_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_VALID_DIR)

    invalid_data_dir: str = os.path.join(
        data_validation_dir, DATA_VALIDATION_INVALID_DIR
    )

    valid_train_file_path: str = os.path.join(valid_data_dir, TRAIN_FILE_NAME)

    valid_test_file_path: str = os.path.join(valid_data_dir, TEST_FILE_NAME)

    invalid_train_file_path: str = os.path.join(invalid_data_dir, TRAIN_FILE_NAME)

    invalid_test_file_path: str = os.path.join(invalid_data_dir, TEST_FILE_NAME)

    drift_report_file_path: str = os.path.join(
        data_validation_dir,
        DATA_VALIDATION_DRIFT_REPORT_DIR,
        DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
    )


@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME
    )

    transformed_train_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        TRAIN_FILE_NAME.replace("csv", "npy"),
    )

    transformed_test_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        TEST_FILE_NAME.replace("csv", "npy"),
    )

    transformed_object_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
        PREPROCSSING_OBJECT_FILE_NAME,
    )


@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME
    )

    trained_model_file_path: str = os.path.join(
        model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR, MODEL_FILE_NAME
    )

    expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE

    model_config_file_path: str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH


@dataclass
class ModelEvaluationConfig:
    changed_threshold_score: float = MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE

    bucket_name: str = MODEL_PUSHER_BUCKET_NAME

    s3_model_key_path: str = os.path.join(MODEL_PUSHER_S3_KEY, MODEL_FILE_NAME)


@dataclass
class ModelPusherConfig:
    bucket_name: str = MODEL_PUSHER_BUCKET_NAME

    s3_model_key_path: str = os.path.join(MODEL_PUSHER_S3_KEY, MODEL_FILE_NAME)


@dataclass
class PredictionPipelineConfig:
    data_bucket_name: str = prediction_pipeline.PREDICTION_DATA_BUCKET

    data_file_path: str = prediction_pipeline.PREDICTION_INPUT_FILE_NAME

    model_file_path: str = os.path.join(MODEL_PUSHER_S3_KEY, MODEL_FILE_NAME)

    model_bucket_name: str = prediction_pipeline.MODEL_BUCKET_NAME

    output_file_name: str = prediction_pipeline.PREDICTION_OUTPUT_FILE_NAME


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float

    best_model_f1_score: float

    is_model_accepted: bool

    changed_accuracy: float

    best_model_metric_artifact: ClassificationMetricArtifact
