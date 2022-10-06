import logging
import os
import pickle
import sys
from io import StringIO

import boto3
from botocore.exceptions import ClientError
from pandas import read_csv

from sensor.exception import SensorException
from sensor.utils.read_params import read_params

logger = logging.getLogger(__name__)


class S3Operation:
    def __init__(self):

        self.config = read_params()

        self.file_format = self.config["save_format"]

        self.s3_client = boto3.client("s3")

        self.s3_resource = boto3.resource("s3")

    def read_object(self, object, decode=True, make_readable=False):
        logger.info("Entered the read_object method of S3Operations class")
        try:
            func = (
                lambda: object.get()["Body"].read().decode()
                if decode is True
                else object.get()["Body"].read()
            )

            conv_func = lambda: StringIO(func()) if make_readable is True else func()

            logger.info("Exited the read_object method of S3Operations class")

            return conv_func()

        except Exception as e:
            raise SensorException(e, sys) from e

    def get_bucket(self, bucket):
        logger.info("Entered the get_bucket method of S3Operations class")

        try:
            bucket = self.s3_resource.Bucket(bucket)

            logger.info("Exited the get_bucket method of S3Operations class")

            return bucket

        except Exception as e:
            raise SensorException(e, sys) from e

    def get_file_object(self, fname, bucket):
        logger.info("Entered the get_file_object method of S3Operations class")

        try:
            bucket = self.get_bucket(bucket)

            lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(lst_objs)

            logger.info("Exited the get_file_object method of S3Operations class")

            return file_objs

        except Exception as e:
            raise SensorException(e, sys) from e

    def load_model(self, model_name, bucket, model_dir=None):
        logger.info("Entered the load_model method of S3Operations class")

        try:
            func = (
                lambda: model_name + self.file_format
                if model_dir is None
                else model_dir + "/" + model_name + self.file_format
            )

            model_file = func()

            f_obj = self.get_file_object(model_file, bucket)

            model_obj = self.read_object(f_obj, decode=False)

            model = pickle.loads(model_obj)

            logger.info("Exited the load_model method of S3Operations class")

            return model

        except Exception as e:
            raise SensorException(e, sys) from e

    def create_folder(self, folder_name, bucket):
        logger.info("Entered the create_folder method of S3Operations class")

        try:
            self.s3_resource.Object(bucket, folder_name).load()

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name + "/"

                self.s3_client.put_object(Bucket=bucket, Key=folder_obj)

            else:
                pass
            logger.info("Exited the create_folder method of S3Operations class")

    def upload_file(self, from_fname, to_fname, bucket, remove=True):
        logger.info("Entered the upload_file method of S3Operations class")
        try:
            self.s3_resource.meta.client.upload_file(from_fname, bucket, to_fname)

            if remove is True:
                os.remove(from_fname)

            else:
                pass
            logger.info("Exited the upload_file method of S3Operations class")

        except Exception as e:
            raise SensorException(e, sys) from e

    def upload_folder(self, folder, bucket):
        logger.info("Entered the upload_folder method of S3Operations class")

        try:
            lst = os.listdir(folder)

            for f in lst:
                local_f = os.path.join(folder, f)

                dest_f = f

                self.upload_file(local_f, dest_f, bucket, remove=False)

            logger.info("Exited the upload_folder method of S3Operations class")

        except Exception as e:
            raise SensorException(e, sys) from e

    def upload_df_as_csv(self, data_frame, local_fname, bucket_fname, bucket):
        logger.info("Entered the upload_df_as_csv method of S3Operations class")

        try:
            data_frame.to_csv(local_fname, index=None, header=True)

            self.upload_file(local_fname, bucket_fname, bucket)

            logger.info("Exited the upload_df_as_csv method of S3Operations class")

        except Exception as e:
            raise SensorException(e, sys) from e

    def get_df_from_object(self, object):
        logger.info("Entered the get_df_from_object method of S3Operations class")

        try:
            content = self.read_object(object, make_readable=True)

            df = read_csv(content, na_values="na")

            logger.info("Exited the get_df_from_object method of S3Operations class")

            return df

        except Exception as e:
            raise SensorException(e, sys) from e

    def read_csv(self, fname, bucket):
        logger.info("Entered the read_csv method of S3Operations class")

        try:
            csv_obj = self.get_file_object(fname, bucket)

            df = self.get_df_from_object(csv_obj)

            logger.info("Exited the read_csv method of S3Operations class")

            return df

        except Exception as e:
            raise SensorException(e, sys) from e
