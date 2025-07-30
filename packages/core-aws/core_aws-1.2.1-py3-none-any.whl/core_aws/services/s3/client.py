# -*- coding: utf-8 -*-

from io import BytesIO
from typing import Dict, Iterator, List

from botocore.client import Config
from botocore.exceptions import ClientError

from core_aws.services.base import AwsClient
from core_aws.services.base import AwsClientException


class S3Client(AwsClient):
    """ Client for S3 Service """

    def __init__(self, signature_version: str = "s3v4", **kwargs):
        super().__init__(
            service="s3",
            config=Config(signature_version=signature_version),
            **kwargs
        )

    def does_bucket_exist(self, bucket: str) -> bool:
        """ It checks if the bucket exist or not """

        try:
            self.client.list_objects_v2(Bucket=bucket, MaxKeys=1)
            return True

        except ClientError as error:
            # If a specific error indicating the bucket does not exist is raised, return False
            if error.response["Error"]["Code"] == "NoSuchBucket":
                return False

            else:
                # If any other error occurs, raise it
                raise error

    def list_objects(self, bucket: str, prefix: str = "", **kwargs) -> Dict:
        """
        Retrieve information of objects (files) into s3 bucket...
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects

        :param bucket: Bucket name.
        :param prefix: Objects prefix.
        :param kwargs:

        :return:

            .. code-block:: python

                {
                    "IsTruncated": True|False,
                    "Marker": "string",
                    "NextMarker": "string",
                    "Contents": [
                        {
                            "Key": "string",
                            "LastModified": datetime(2015, 1, 1),
                            "ETag": "string",
                            "ChecksumAlgorithm": [
                                "CRC32"|"CRC32C"|"SHA1"|"SHA256",
                            ],
                            "Size": 123,
                            "StorageClass": "STANDARD" | ... | "GLACIER" ",
                            "Owner": {
                                "DisplayName": "string",
                                "ID": "string"
                            },
                            "RestoreStatus": {
                                "IsRestoreInProgress": True|False,
                                "RestoreExpiryDate": datetime(2015, 1, 1)
                            }
                        },
                    ],
                    "Name": "string",
                    "Prefix": "string",
                    "Delimiter": "string",
                    "MaxKeys": 123,
                    "CommonPrefixes": [
                        {
                            "Prefix": "string"
                        },
                    ],
                    "EncodingType": "url",
                    "RequestCharged": "requester"
                }
            ..
        """

        try:
            return self.client.list_objects(Bucket=bucket, Prefix=prefix, **kwargs)

        except Exception as error:
            raise AwsClientException(error)

    def list_all_objects(self, bucket: str, prefix: str, **kwargs) -> Iterator[Dict]:
        """
        Retrieve information of all objects (files) into s3 bucket. This way you don"t need
        to worry about pagination...

        :param bucket: Bucket name.
        :param prefix: Objects prefix.
        :param kwargs:

        :return: An iterator that contains dictionaries with the following structure

            .. code-block:: python

                {
                    "Key": "string",
                    "LastModified": datetime(2015, 1, 1),
                    "ETag": "string",
                    "ChecksumAlgorithm": [
                        "CRC32"|"CRC32C"|"SHA1"|"SHA256",
                    ],
                    "Size": 123,
                    "StorageClass": "STANDARD" | ... | "GLACIER" ",
                    "Owner": {
                        "DisplayName": "string",
                        "ID": "string"
                    },
                    "RestoreStatus": {
                        "IsRestoreInProgress": True|False,
                        "RestoreExpiryDate": datetime(2015, 1, 1)
                    }
                }
            ..
        """

        new_kwargs = {"Bucket": bucket, "Prefix": prefix, **kwargs}
        is_truncated = True
        latest_key = None

        try:
            while is_truncated:
                res = self.client.list_objects(**new_kwargs)
                for record in res.get("Contents", []):
                    latest_key = record["Key"]
                    yield record

                is_truncated = res.get("IsTruncated", False)
                if is_truncated:
                    new_kwargs["Marker"] = latest_key

        except Exception as error:
            raise AwsClientException(error)

    def upload_file(self, bucket: str, key: str, path: str, **kwargs):
        """
        Upload a file to AWS bucket...
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/upload_file.html

        :param bucket: The bucket name of the bucket containing the object.
        :param key: Key/path of the object.
        :param path: (str) -- The path to the file to upload.
        :param kwargs:

        :return:
        """

        try:
            return self.client.upload_file(
                Filename=path,
                Bucket=bucket, Key=key,
                **kwargs)

        except Exception as error:
            raise AwsClientException(error)

    def upload_object(self, bucket: str, key: str, data: BytesIO,  **kwargs):
        """
        Upload a file (in form StringIO) to AWS bucket...
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_fileobj

        :param bucket: The bucket name of the bucket containing the object.
        :param key: Key/path of the object.

        :param data:
            A file-like object to upload. At a minimum, it must implement the
            read method, and must return bytes.

        :param kwargs:

        :return:
        """

        try:
            return self.client.upload_fileobj(
                Fileobj=data,
                Bucket=bucket, Key=key,
                **kwargs)

        except Exception as error:
            raise AwsClientException(error)

    def download_file(self, bucket: str, key: str, local_path: str, **kwargs) -> str:
        """
        Download file from the S3 bucket to the local path...
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/download_file.html

        :param local_path: Path to save the file locally.
        :param bucket: The bucket name of the bucket containing the object.
        :param key: Key/path of the object.
        :param kwargs:

        :return: The local file where the file was stored.
        """

        try:
            self.client.download_file(Bucket=bucket, Key=key, Filename=local_path, **kwargs)
            return local_path

        except Exception as error:
            raise AwsClientException(error)

    def download_object(self, buffer: BytesIO, bucket: str, key: str, **kwargs) -> None:
        """
        Download an object from S3 to a file-like object. The file-like object must
        be in binary mode...

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/download_fileobj.html

        :param bucket: The bucket name of the bucket containing the object.
        :param key: Key/path of the object.

        :param buffer:
            (a file-like object) -- A file-like object to
            download into. At a minimum, it must implement
            the write method and must accept bytes.

        :param kwargs:
        """

        try:
            return self.client.download_fileobj(
                Bucket=bucket, Key=key,
                Fileobj=buffer,
                **kwargs)

        except Exception as error:
            raise AwsClientException(error)

    def copy(self, copy_source: Dict, bucket: str, key: str, **kwargs):
        """
        Copy an object from one S3 location to another. This is a managed transfer which will
        perform a multipart copy in multiple threads if necessary...

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Bucket.copy

        :type copy_source: dict
        :param copy_source: The name of the source bucket, key name of the
            source object, and optional version ID of the source object. The
            dictionary format is:
            ``{"Bucket": "bucket", "Key": "key", "VersionId": "id"}``. Note
            that the ``VersionId`` key is optional and may be omitted.

        :type bucket: str
        :param bucket: The name of the bucket to copy to

        :type key: str
        :param key: The name of the key to copy to

        :param kwargs: Extra arguments.
            ExtraArgs: dict -- Extra arguments that may be passed to the client operation

            Callback: function
                A method which takes a number of bytes transferred to
                be periodically called during the copy.

            SourceClient: botocore or boto3 Client
                The client to be used for operation that
                may happen at the source object. For example, this client is
                used for the head_object that determines the size of the copy.
                If no client is provided, the current client is used as the client
                for the source object.

            ConfigLoader: boto3.s3.transfer.TransferConfig
                The transfer configuration to be used when performing
                the copy.

        :return:
        """

        try:
            return self.client.copy(
                CopySource=copy_source,
                Bucket=bucket, Key=key,
                **kwargs)

        except Exception as error:
            raise AwsClientException(error)

    def delete_object(self, bucket: str, key: str, **kwargs) -> Dict:
        """
        Delete objects from a bucket using a single request...
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/delete_object.html

        :param bucket: The bucket name of the bucket containing the object.
        :param key: Key name of the object to delete.
        :param kwargs:

        :return:

            .. code-block:: python

                {
                    "DeleteMarker": True|False,
                    "VersionId": "string",
                    "RequestCharged": "requester"
                }
            ..
        """

        try:
            return self.client.delete_object(
                Bucket=bucket, Key=key,
                **kwargs)

        except Exception as error:
            raise AwsClientException(error)

    def delete_objects(self, bucket: str, objects: List[Dict], **kwargs) -> Dict:
        """
        Delete objects from a bucket using a single request...
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/delete_objects.html

        :param bucket:
        :param objects: The objects to delete...
            Object Identifier is unique value to identify objects.
            Key (string) [REQUIRED] -> Key name of the object to delete.
            VersionId (string) -> VersionId for the specific version of the object to delete.

            Example...

                .. code-block:: python

                    [{
                        "Key": "some_file.csv",
                        "VersionId": "6LGg7gQLhY41.maGB5Z6SWW.dcq0vx7b",
                    }]
                ..

        :param kwargs:

        :return:

            .. code-block:: python

                {
                    "Deleted": [
                        {
                            "Key": "string",
                            "VersionId": "string",
                            "DeleteMarker": True|False,
                            "DeleteMarkerVersionId": "string"
                        },
                    ],
                    "RequestCharged": "requester",
                    "Errors": [
                        {
                            "Key": "string",
                            "VersionId": "string",
                            "Code": "string",
                            "Message": "string"
                        },
                    ]
                }
            ..
        """

        if not objects:
            return {}

        try:
            return self.client.delete_objects(
                Bucket=bucket,
                Delete={"Objects": objects},
                **kwargs)

        except Exception as error:
            raise AwsClientException(error)
