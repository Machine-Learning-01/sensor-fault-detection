import json
import sys
from typing import Tuple, Union

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from pandas import DataFrame

from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import MainUtils
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        self.train_set = train_set

        self.test_set = test_set
        self.data_ingestion_artifact = data_ingestion_artifact
        self.validation_status = False
        self.utils = MainUtils()
        self._schema_config = self.utils.read_yaml_file(filename=SCHEMA_FILE_PATH)

    def validate_schema_columns(self, df: DataFrame) -> bool:
        """
        Method Name :   validate_schema_columns
        Description :   This method validates the schema columns for the particular dataframe 
        
        Output      :   True or False value is returned based on the schema 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:
            if len(df.columns) == len(self._schema_config["columns"]):
                validation_status = True

            else:
                validation_status = False

            return validation_status

        except Exception as e:
            raise SensorException(e, sys) from e

    def validate_schema_for_numerical_datatype(self, df: DataFrame) -> bool:
        """
        Method Name :   validate_schema_for_numerical_datatype
        Description :   This method validates the schema for numerical datatype 
        
        Output      :   True or False value is returned based on the schema 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:
            for column in self._schema_config["numerical_columns"]:
                if column in df.columns:
                    validation_status = True
                else:
                    validation_status = False

            return validation_status

        except Exception as e:
            raise SensorException(e, sys) from e

    def validate_dataset_schema_columns(self) -> Tuple[bool, bool]:
        """
        Method Name :   validate_dataset_schema_columns
        Description :   This method validates the schema for schema columns for both train and test set 
        
        Output      :   True or False value is returned based on the schema 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info(
            "Entered validate_dataset_schema_columns method of Data_Validation class"
        )

        try:
            logging.info("Validating dataset schema columns")

            train_schema_status = self.validate_schema_columns(self.train_set)

            logging.info("Validated dataset schema columns on the train set")

            test_schema_status = self.validate_schema_columns(self.test_set)

            logging.info("Validated dataset schema columns on the test set")

            logging.info("Validated dataset schema columns")

            return train_schema_status, test_schema_status

        except Exception as e:
            raise SensorException(e, sys) from e

    def validate_dataset_schema_for_numerical_datatype(self) -> Tuple[bool, bool]:
        """
        Method Name :   validate_dataset_schema_for_numerical_datatype
        Description :   This method validates the schema for numerical datatype for both train and test set 
        
        Output      :   True or False value is returned based on the schema 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info(
            "Entered validate_dataset_schema_for_numerical_datatype method of Data_Validation class"
        )

        try:
            logging.info("Validating dataset schema for numerical datatype")

            train_num_datatype_status = self.validate_schema_for_numerical_datatype(
                self.train_set
            )

            logging.info(
                "Validated dataset schema for numerical datatype for train set"
            )

            test_num_datatype_status = self.validate_schema_for_numerical_datatype(
                self.test_set
            )

            logging.info("Validated dataset schema for numerical datatype for test set")

            logging.info(
                "Exited validate_dataset_schema_for_numerical_datatype method of Data_Validation class"
            )

            return train_num_datatype_status, test_num_datatype_status

        except Exception as e:
            raise SensorException(e, sys) from e

    def detect_dataset_drift(
        self, reference: DataFrame, production: DataFrame, get_ratio: bool = False
    ) -> Union[bool, float]:
        """
        Method Name :   detect_dataset_drift
        Description :   This method detects the dataset drift using the reference and production dataframe 
        
        Output      :   Returns bool or float value based on the get_ration parameter
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])

            data_drift_profile.calculate(reference, production)

            report = data_drift_profile.json()

            json_report = json.loads(report)

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]

            n_drifted_features = json_report["data_drift"]["data"]["metrics"][
                "n_drifted_features"
            ]

            if get_ratio:
                return n_drifted_features / n_features

            else:
                return json_report["data_drift"]["data"]["metrics"]["dataset_drift"]

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
        logging.info("Entered initiate_data_validation method of Data_Validation class")

        try:
            logging.info("Initiated data validation for the dataset")

            schema_train_col_status,schema_test_col_status = self.validate_dataset_schema_columns()
            logging.info(
                f"Schema train cols status is {schema_train_col_status} and schema test cols status is {schema_test_col_status}"
            )
            logging.info("Validated dataset schema columns")
            schema_train_num_cols_status,schema_test_num_cols_status= self.validate_dataset_schema_for_numerical_datatype()
            logging.info(
                f"Schema train numerical cols status is {schema_train_num_cols_status} and schema test numerical cols status is {schema_test_num_cols_status}"
            )

            logging.info("Validated dataset schema for numerical datatype")
            status = (
                schema_train_num_cols_status is True
                and schema_test_num_cols_status is True
                and schema_train_col_status is True
                and schema_test_col_status is True
              
            )
            if status:
                drift = self.detect_dataset_drift(self.train_set, self.test_set)
            status=drift
            data_validation_artifact=   DataValidationArtifact(validation_status=status,
            valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
            valid_test_file_path=self.data_ingestion_artifact.tested_file_path)
            # )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
