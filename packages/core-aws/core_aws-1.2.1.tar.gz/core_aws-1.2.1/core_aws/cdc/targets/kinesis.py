# -*- coding: utf-8 -*-

from typing import List

from core_cdc.base import Record
from core_cdc.targets.base import Target

from core_aws.services.kinesis.client import KinesisClient


class KinesisDataStreamTarget(Target):
    """ Send data to a Kinesis Data Stream """

    def __init__(self, aws_region: str, stream_name: str, partition_key: str, **kwargs):
        super(KinesisDataStreamTarget, self).__init__(**kwargs)

        self.aws_region = aws_region
        self.client = KinesisClient(region=self.aws_region)
        self.partition_key = partition_key
        self.stream_name = stream_name

    @classmethod
    def registered_name(cls) -> str:
        return cls.__name__

    def _save(self, records: List[Record], **kwargs):
        return self.client.send_records(
            records=[x.to_json() for x in records],
            stream_name=self.stream_name,
            partition_key=self.partition_key,
            **kwargs)
