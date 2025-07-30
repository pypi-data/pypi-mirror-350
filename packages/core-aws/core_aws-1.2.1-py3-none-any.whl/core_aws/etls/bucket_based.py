# -*- coding: utf-8 -*-

import os
from abc import ABC, abstractmethod
from typing import Iterator

from core_etl.file_based import IBaseEtlFromFile

from core_aws.etls.base import IBaseEtlOnAWS


class IBaseEtlOnAwsBucket(IBaseEtlFromFile, IBaseEtlOnAWS, ABC):
    """ Base class for ETL processes that retrieves and process files from S3 """

    def __init__(
            self, bucket: str = None, prefix: str = None,
            archive_bucket: str = None, archive_prefix: str = None,
            error_bucket: str = None, error_prefix: str = None,
            **kwargs):

        """
        :param bucket: Bucket that contains the files to process.
        :param prefix: Path within the Bucket to retrieve the files to process.
        :param archive_bucket: Bucket for archiving.
        :param archive_prefix: Path to use in the archiving process.
        :param error_bucket: Bucket for archiving when errors.
        :param error_prefix: Path to use in the archiving process when errors.
        """

        super(IBaseEtlOnAwsBucket, self).__init__(**kwargs)

        self.bucket = bucket
        self.archive_bucket = archive_bucket
        self.error_bucket = error_bucket

        self.prefix = prefix
        self.archive_prefix = archive_prefix
        self.error_prefix = error_prefix

    def _execute(self, *args, **kwargs) -> int:
        self.info(f"Retrieving files from bucket: {self.bucket}, path: {self.prefix}...")
        return super(IBaseEtlOnAwsBucket, self)._execute(*args, **kwargs)

    def get_paths(self, *args, **kwargs) -> Iterator[str]:
        """ It returns the list of keys for the objects within the bucket """

        for rec in self.s3_client.list_all_objects(self.bucket, self.prefix):
            yield rec["Key"]

    def process_file(self, path: str, *args, **kwargs):
        self.info(f"Downloading file: {path}...")
        file_name = path.split('/')[-1]

        local_path = self.s3_client.download_file(
            local_path=f"{self.temp_folder}/{file_name}",
            bucket=self.bucket,
            key=path)

        self.info("Downloaded!")
        final_bucket, final_path = None, None

        try:
            self.info(f"Processing file: {file_name}.")
            self.process_local_file(local_path)
            self.info("Processed!")

        except Exception as error:
            self.error(f"Error: {error}.")
            final_bucket = self.error_bucket
            final_path = self.error_prefix

        else:
            final_bucket = self.archive_bucket
            final_path = self.archive_prefix

        finally:
            if final_bucket and final_path:
                self.info(f"Archiving into bucket: {self.error_bucket}, path: {self.error_prefix}...")

                self.s3_client.copy(
                    copy_source={
                        "Bucket": self.bucket,
                        "Key": path
                    },
                    bucket=self.error_bucket,
                    key=self.error_prefix
                )

                self.info("Done")

            self.info(f"Deleting file: {path} from bucket: {self.bucket}...")
            self.s3_client.delete_object(self.bucket, key=path)
            self.info("File deleted!")
            os.remove(local_path)

    @abstractmethod
    def process_local_file(self, local_path: str, *args, **kwargs):
        """ Do something with the downloaded file """
