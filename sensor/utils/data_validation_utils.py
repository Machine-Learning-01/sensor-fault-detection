import logging
import sys

from sensor.exception import SensorException
from sensor.utils.read_params import read_params

logger = logging.getLogger(__name__)

schema_file = read_params("sensor/config/schema.yaml")


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
        message = SensorException(e, sys)
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
        message = SensorException(e, sys)
        raise message.error_message
