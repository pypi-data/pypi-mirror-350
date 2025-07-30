# -*- coding: utf-8 -*-

from typing import List

from core_cdc.base import Record
from core_cdc.targets.base import Target

from core_aws.services.sns.client import SnsClient
from core_aws.services.sns.client import SnsMessage


class SnsTarget(Target):
    """ To send data to a SQS queue """

    def __init__(self, aws_region: str, topic_arn: str, batch_size: int = 10, **kwargs):
        super(SnsTarget, self).__init__(**kwargs)

        self.aws_region = aws_region
        self.client = SnsClient(region=aws_region, batch_size=batch_size)
        self.topic_arn = topic_arn
        self.execute_ddl = False

    @classmethod
    def registered_name(cls) -> str:
        return cls.__name__

    def _save(self, records: List[Record], **kwargs):
        self.client.publish_batch(
            topic_arn=self.topic_arn,
            messages=[
                SnsMessage(Id=f"{rec.table_name}-{x}", Message=rec.to_json())
                for x, rec in enumerate(records)
            ]
        )
