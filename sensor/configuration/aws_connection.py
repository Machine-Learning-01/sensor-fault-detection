import boto3


class S3Client:
    s3_client = None
    s3_resource = None

    def __init__(self):
        if S3Client.s3_client is None:
            S3Client.s3_client = boto3.client("s3")
        if S3Client.s3_resource is None:
            S3Client.s3_resource = boto3.resource("s3")
        self.s3_client = S3Client.s3_client
        self.s3_resource = S3Client.s3_resource
