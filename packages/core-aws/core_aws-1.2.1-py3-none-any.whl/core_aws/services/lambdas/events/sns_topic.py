# -*- coding: utf-8 -*-

from typing import Dict

from .base import EventRecord, EventSource


class SnsRecord(EventRecord):
    """ It represents and wrap a record coming to Lambda from a SNS topic """

    _source = EventSource.SNS_TOPIC

    # noinspection PyPep8Naming
    def __init__(
            self, EventSource: str, EventSubscriptionArn: str,
            EventVersion: str, Sns: Dict) -> None:

        self._event_source = EventSource
        self._event_subscription_arn = EventSubscriptionArn
        self._event_version = EventVersion
        self._sns = Sns

    @property
    def message_id(self) -> str:
        return self._sns["MessageId"]

    @property
    def message(self) -> str:
        return self._sns["Message"]
