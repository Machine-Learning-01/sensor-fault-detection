import logging
import sys

from scania_truck.exception import ScaniaException
from scania_truck.utils.read_params import read_params

logger = logging.getLogger(__name__)

schema_file = read_params("scania_truck/config/schema.yaml")


def validate_schema_columns(df):
    try:
        try:
            if len(df.columns) == len(schema_file["columns"]):
                validation_status = True

            else:
                validation_status = False

        except Exception as e:
            validation_status = False

        return validation_status

    except Exception as e:
        message = ScaniaException(e, sys)

        logger.error(message.error_message)

        raise message.error_message


def validate_schema_for_numerical_datatype(df):
    try:
        for column in schema_file["numerical_columns"]:
            try:
                if column in df.columns:
                    validation_status = True
                else:
                    validation_status = False

            except:
                validation_status = False

        return validation_status

    except Exception as e:
        message = ScaniaException(e, sys)

        logger.error(message.error_message)

        raise message.error_message
