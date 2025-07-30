# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Type

try:
    from typing import Self

except ImportError:
    # For earlier versions...
    from typing_extensions import Self


class EventSource(str, Enum):
    KINESIS_DATA_STREAM = "aws:kinesis"
    SNS_TOPIC = "aws:sns"
    SQS_QUEUE = "aws:sqs"


class EventRecord(ABC):
    """
    Base class for a record that comes into the Lambda Event within
    the attribute "Records"...
    """

    _subclasses: Dict[str, Type[Self]] = {}
    _source: EventSource

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._subclasses[cls._source] = cls

    @property
    @abstractmethod
    def message_id(self) -> str:
        """ It returns the message_id """

    @property
    @abstractmethod
    def message(self) -> str:
        """ It returns the message data """

    @classmethod
    def from_dict(cls, message: Dict) -> Self | Dict:
        """
        It creates a "Message" object...

        :param message: Raw data for the message coming from the source.
        :return: A "Message" object or the raw message if the wrapper is not implemented.
        """

        cls_ = cls._subclasses.get(message.get("eventSource") or message.get("EventSource") or None)
        if not cls_:
            return message

        return cls_(**message)
