import logging
import os
import pickle
import sys
from io import StringIO
from pandas import read_csv

import boto3
from botocore.exceptions import ClientError

from scania_truck.exception import ScaniaException
from scania_truck.utils.read_params import read_params

logger = logging.getLogger(__name__)


class S3Operation:
    def __init__(self):

        self.config = read_params()

        self.file_format = self.config["save_format"]

        self.s3_client = boto3.client("s3")

        self.s3_resource = boto3.resource("s3")

    def read_object(self, object, decode=True, make_readable=False):
        try:
            func = (
                lambda: object.get()["Body"].read().decode()
                if decode is True
                else object.get()["Body"].read()
            )

            conv_func = lambda: StringIO(func()) if make_readable is True else func()

            return conv_func()

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def get_bucket(self, bucket):
        # self.log_writer.info("Entered get_bucket method of S3Operation class")

        try:
            bucket = self.s3_resource.Bucket(bucket)

            return bucket

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def get_file_object(self, fname, bucket):
        try:
            bucket = self.get_bucket(bucket)

            lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(lst_objs)

            return file_objs

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def load_model(self, model_name, bucket, model_dir=None):
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

            return model

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def create_folder(self, folder_name, bucket):
        try:
            self.s3_resource.Object(bucket, folder_name).load()

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name + "/"

                self.s3_client.put_object(Bucket=bucket, Key=folder_obj)

            else:
                pass

    def upload_file(self, from_fname, to_fname, bucket, remove=True):
        try:
            self.s3_resource.meta.client.upload_file(from_fname, bucket, to_fname)

            if remove is True:
                os.remove(from_fname)

            else:
                pass

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def upload_folder(self, folder, bucket):
        try:
            lst = os.listdir(folder)

            for f in lst:
                local_f = os.path.join(folder, f)

                dest_f = f

                self.upload_file(local_f, dest_f, bucket, remove=False)

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def upload_df_as_csv(self, data_frame, local_fname, bucket_fname, bucket):
        try:
            data_frame.to_csv(local_fname, index=None, header=True)

            self.upload_file(local_fname, bucket_fname, bucket)

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def get_df_from_object(self, object):
        try:
            content = self.read_object(object, make_readable=True)

            df = read_csv(content)

            return df

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message

    def read_csv(self, fname, bucket):
        try:
            csv_obj = self.get_file_object(fname, bucket)

            df = self.get_df_from_object(csv_obj,)

            return df

        except Exception as e:
            message = ScaniaException(e, sys)

            logger.error(message.error_message)

            raise message.error_message
