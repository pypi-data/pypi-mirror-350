# -*- coding: utf-8 -*-

from typing import Dict

from .base import EventRecord, EventSource


class SqsRecord(EventRecord):
    """ It represents and wrap a record coming to Lambda from a SQS queue """

    _source = EventSource.SQS_QUEUE

    # noinspection PyPep8Naming
    def __init__(
            self, eventSource: str, eventSourceARN: str, awsRegion: str, messageId: str,
            receiptHandle: str, body: str, md5OfBody: str, attributes: Dict,
            md5OfMessageAttributes: str, messageAttributes: Dict) -> None:

        self._event_source = eventSource
        self._event_source_arn = eventSourceARN
        self._aws_region = awsRegion

        self._message_id = messageId
        self._receipt_handle = receiptHandle
        self._body = body

        self._attributes = attributes
        self._messageAttributes = messageAttributes

        self._md5_of_body = md5OfBody
        self._md5OfMessageAttributes = md5OfMessageAttributes

    @property
    def message_id(self) -> str:
        return self._message_id

    @property
    def message(self) -> str:
        return self._body
