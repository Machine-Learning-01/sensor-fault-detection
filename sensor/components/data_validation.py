import json
import sys

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import MainUtils


class DataValidation:
    def __init__(self, train_set, test_set):
        self.train_set = train_set

        self.test_set = test_set

        self.validation_status = False

        self.utils = MainUtils()

        self._schema_config = self.utils.read_schema_config_file()

    def validate_schema_columns(self, df):
        try:
            if len(df.columns) == len(self._schema_config["columns"]):
                validation_status = True

            else:
                validation_status = False

            return validation_status

        except Exception as e:
            raise SensorException(e, sys) from e

    def validate_schema_for_numerical_datatype(self, df):
        try:
            for column in self._schema_config["numerical_columns"]:
                if column in df.columns:
                    validation_status = True
                else:
                    validation_status = False

            return validation_status

        except Exception as e:
            raise SensorException(e, sys) from e

    def validate_dataset_schema_columns(self):
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

    def validate_dataset_schema_for_numerical_datatype(self):
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

    @staticmethod
    def detect_dataset_drift(reference, production, get_ratio=False):
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

    def initiate_data_validation(self):
        logging.info("Entered initiate_data_validation method of Data_Validation class")

        try:
            logging.info("Initiated data validation for the dataset")

            (
                schema_train_col_status,
                schema_test_col_status,
            ) = self.validate_dataset_schema_columns()

            logging.info(
                f"Schema train cols status is {schema_train_col_status} and schema test cols status is {schema_test_col_status}"
            )

            logging.info("Validated dataset schema columns")

            (
                schema_train_num_cols_status,
                schema_test_num_cols_status,
            ) = self.validate_dataset_schema_for_numerical_datatype()

            logging.info(
                f"Schema train numerical cols status is {schema_train_num_cols_status} and schema test numerical cols status is {schema_test_num_cols_status}"
            )

            logging.info("Validated dataset schema for numerical datatype")

            if (
                schema_train_num_cols_status is True
                and schema_test_num_cols_status is True
                and schema_train_col_status is True
                and schema_test_col_status is True
            ):

                logging.info("Dataset schema validation completed")

                return True

            else:
                return False

        except Exception as e:
            raise SensorException(e, sys) from e
