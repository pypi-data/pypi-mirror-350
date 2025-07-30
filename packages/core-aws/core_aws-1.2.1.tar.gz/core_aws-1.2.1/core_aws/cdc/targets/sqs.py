# -*- coding: utf-8 -*-

import json
from typing import List
from uuid import uuid4

from core_cdc.base import Record
from core_cdc.targets.base import Target
from core_mixins.utils import get_batches

from core_aws.services.sqs.client import SqsClient


class SqsTarget(Target):
    """ To send data to a SQS queue """

    def __init__(self, aws_region: str, queue_name: str, **kwargs):
        super(SqsTarget, self).__init__(**kwargs)

        self.aws_region = aws_region
        self.execute_ddl = False
        self.queue_url = None

        self.queue_name = queue_name
        self.client = SqsClient(region=aws_region)
        self.queue_url = None

    @classmethod
    def registered_name(cls) -> str:
        return cls.__name__

    def init_client(self, **kwargs) -> None:
        self.queue_url = self.client.get_queue_by_name(self.queue_name).url

    def _save(self, records: List[Record], **kwargs):
        for batch in get_batches([x.to_json() for x in records], 10):
            self.client.send_message_batch(
                queue_url=self.queue_url,
                entries=[
                    {
                        "Id": str(uuid4()),
                        "MessageBody": json.dumps(entry),
                        "DelaySeconds": 0,
                        # "MessageDeduplicationId": "",
                        # "MessageGroupId": ""
                    } for entry in batch
                ]
            )
