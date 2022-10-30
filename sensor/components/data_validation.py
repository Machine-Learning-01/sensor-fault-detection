import json
import sys

import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from pandas import DataFrame

from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        """

        :param dataframe:
        :return: True if required columns present
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])

            logging.info(f"Is required column present: [{status}]")

            return status

        except Exception as e:
            raise SensorException(e, sys)

    def is_numerical_column_exist(self, df: DataFrame) -> bool:
        """
        This function check numerical column is present in dataframe or not
        :param df:
        :return: True if all column presents else False
        """
        try:
            dataframe_columns = df.columns

            status = True

            missing_numerical_columns = []

            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    status = False

                    missing_numerical_columns.append(column)

            logging.info(f"Missing numerical column: {missing_numerical_columns}")

            return status

        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)

    def detect_dataset_drift(
        self, reference_df: DataFrame, current_df: DataFrame,
    ) -> bool:
        """
        :param reference_df: base dataframe
        :param current_df: current dataframe
        :return: True of drift detected else false
        """
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])

            data_drift_profile.calculate(reference_df, current_df)

            report = data_drift_profile.json()

            json_report = json.loads(report)

            write_yaml_file(
                file_path=self.data_validation_config.drift_report_file_path,
                content=json_report,
            )

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]

            n_drifted_features = json_report["data_drift"]["data"]["metrics"][
                "n_drifted_features"
            ]

            logging.info(f"{n_drifted_features}/{n_features} drift detected.")

            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]

            return drift_status

        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:
            validation_error_msg = ""

            logging.info("Starting data validation")

            train_df = DataValidation.read_data(
                file_path=self.data_ingestion_artifact.trained_file_path
            )

            test_df = DataValidation.read_data(
                file_path=self.data_ingestion_artifact.test_file_path
            )

            status = self.validate_number_of_columns(dataframe=train_df)

            logging.info(
                f"All required columns present in training dataframe: {status}"
            )

            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."

            status = self.validate_number_of_columns(dataframe=test_df)

            logging.info(f"All required columns present in testing dataframe: {status}")

            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."

            status = self.is_numerical_column_exist(df=train_df)

            if not status:
                validation_error_msg += (
                    f"Numerical columns are missing in training dataframe."
                )

            status = self.is_numerical_column_exist(df=test_df)

            if not status:
                validation_error_msg += (
                    f"Numerical columns are missing in test dataframe."
                )

            validation_status = len(validation_error_msg) == 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)

                if drift_status:
                    logging.info(f"Drift detected.")

            else:
                logging.info(f"Validation_error: {validation_error_msg}")

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys) from e
