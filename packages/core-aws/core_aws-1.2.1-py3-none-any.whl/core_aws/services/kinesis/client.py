# -*- coding: utf-8 -*-

import json
from time import sleep
from typing import ByteString, List, Dict

from core_mixins.utils import get_batches

from core_aws.services.base import AwsClient
from core_aws.services.base import AwsClientException


class KinesisClient(AwsClient):
    """ Client for Kinesis Service """

    def __init__(self, region, **kwargs):
        super().__init__("kinesis", region_name=region, **kwargs)

    def put_record(self, stream_name: str, data: ByteString, partition_key: str, **kwargs) -> Dict:
        """
        Writes a single data record into an Amazon Kinesis data stream. Calling PutRecord
        to send data into the stream for real-time ingestion and subsequent processing, one
        record at a time. Each shard can support writes up to 1,000 records per second, up
        to a maximum data write total of 1 MiB per second...

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/put_record.html

        :param stream_name: The name of the stream to put the data record into.
        :param partition_key: Determines which shard in the stream the data record is assigned to.

        :param data:
            The data blob to put into the record, which is base64-encoded when
            the blob is serialized. When the data blob (the payload before base64-encoding)
            is added to the partition key size, the total size must not exceed the
            maximum record size (1 MiB).

        :param kwargs:
            * ExplicitHashKey: The hash value used to explicitly determine the shard the data
              record is assigned to by overriding the partition key hash.
            * SequenceNumberForOrdering: Guarantees strictly increasing sequence
              numbers, for puts from the same client and to the same partition key.

        :return: It returns a dict with the following structure.

            .. code-block:: python

                {
                    "ShardId": "string",
                    "SequenceNumber": "string",
                    "EncryptionType": "NONE" | "KMS"
                }
            ..
        """

        try:
            return self.client.put_record(
                StreamName=stream_name, Data=data,
                PartitionKey=partition_key, **kwargs)

        except Exception as error:
            raise AwsClientException(error)

    def put_records(self, stream_name: str, records: List[Dict]) -> Dict:
        """
        Writes multiple data records into a Kinesis data stream in a single
        call (also referred to as a PutRecords request). Use this operation to
        send data into the stream for data ingestion and processing.

        Each PutRecords request can support up to 500 records. Each record in the
        request can be as large as 1 MiB, up to a limit of 5 MiB for the entire
        request, including partition keys. Each shard can support writes up to 1,000
        records per second, up to a maximum data write total of 1 MiB per second...

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/put_records.html

        :param stream_name: The name of the stream to put the data record into.
        :param records: The records associated with the request.

        The structure of each record should be:

            .. code-block:: python

                {
                    "Data": b"bytes",
                    "ExplicitHashKey": "string",
                    "PartitionKey": "string"
                }
            ..

        :return: It returns a dict.

            .. code-block:: python

                {
                    "FailedRecordCount": 0,
                    "Records": [
                        {
                            "SequenceNumber": "string",
                            "ShardId": "string",
                            "ErrorCode": "string",
                            "ErrorMessage": "string"
                        },
                    ],
                    "EncryptionType": "NONE" | "KMS"
                }
            ..
        """

        try:
            return self.client.put_records(Records=records, StreamName=stream_name)

        except Exception as error:
            raise AwsClientException(error)

    def send_records(
            self, records: List[Dict], stream_name: str, partition_key: str,
            records_per_request: int = 500, max_attempts: int = 10,
            interval_between_attempt: int = 1):

        """
        Send records to Kinesis Stream. It's like a "high level" implementation that can be
        used instead of "put_records" because it will handle the possible errors and
        will retry the requests...

        :param records: Records to send.
        :param stream_name: Kinesis Stream target.
        :param partition_key: Kinesis partition key.
        :param records_per_request: Number of records to send per request.
        :param max_attempts: Maximum attempts in case of errors.
        :param interval_between_attempt: Seconds between attempts.

        :return: True in case of successful execution.
        """

        return self._send_to_kinesis_stream(
            stream_name=stream_name,
            records=[
                {
                    "Data": json.dumps(record),
                    "PartitionKey": partition_key
                } for record in records
            ],
            records_per_request=records_per_request,
            interval_between_attempt=interval_between_attempt,
            max_attempts=max_attempts)

    def _send_to_kinesis_stream(
            self, records: List[Dict], stream_name: str, records_per_request: int = 500,
            max_attempts: int = 10, interval_between_attempt: int = 1):

        """
        Internal implementation to send request to Kinesis and retry in case of
        the failures...

        :param records: List of records in the form:

            .. code-block:: python

                [{
                    "Data": b"bytes",
                    "ExplicitHashKey": "string",
                    "PartitionKey": "string"
                }]
            ..

        :param stream_name: Kinesis Data Stream name.
        :param records_per_request: Number of records to send per request.
        :param max_attempts: Maximum attempts in case of errors.
        :param interval_between_attempt: Seconds between attempts.

        :return:
        """

        if not records:
            return

        for chunk_ in get_batches(records, records_per_request):
            res = self.put_records(stream_name, chunk_)
            attempt = 1

            while res.get("FailedRecordCount", 0) > 0 and attempt <= max_attempts:
                sleep(interval_between_attempt * attempt)

                # Only send new records...
                chunk_ = [
                    chunk_[x] for x, data in enumerate(res.get("Records", []))
                    if data.get("ErrorCode", False)
                ]

                res = self.put_records(stream_name, chunk_)
                attempt += 1

            if res["FailedRecordCount"] > 0:
                raise AwsClientException("Failed sending data to Kinesis!")
