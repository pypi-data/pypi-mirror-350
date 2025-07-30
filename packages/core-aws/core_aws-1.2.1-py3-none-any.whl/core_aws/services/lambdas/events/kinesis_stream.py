# -*- coding: utf-8 -*-

import base64
from typing import Dict

from .base import EventRecord, EventSource


class KinesisRecord(EventRecord):
    """ It represents and wrap a record coming to Lambda from a Kinesis Data Stream """

    _source = EventSource.KINESIS_DATA_STREAM

    # noinspection PyPep8Naming
    def __init__(
            self, kinesis: Dict, eventSource: str, eventVersion: str, eventID: str,
            eventName: str, invokeIdentityArn: str, awsRegion: str,
            eventSourceARN: str) -> None:
        
        """
        :param kinesis:
            This is the structure of the attribute. The data attribute contains the
            information encoded in base64...

            {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "binlog",
                "sequenceNumber": "49647175778160097793486557372840800878012000746547970050",
                "data": b"eyJldmVudF90aW1lc3RhbXAiOiAxNzAxNDY4MjkwLCA",
                "approximateArrivalTimestamp": 1002071427.66
            }
        """
        
        self._aws_region = awsRegion
        self._invoke_identity_arn = invokeIdentityArn
        self._kinesis = kinesis
        
        self._event_name = eventName
        self._event_source = eventSource
        self._event_source_arn = eventSourceARN
        self._event_version = eventVersion
        self._event_id = eventID
        
    @property
    def message_id(self) -> str:
        return self._event_id

    @property
    def message(self) -> str:
        return base64.b64decode(self._kinesis["data"]).decode()
