# -*- coding: utf-8 -*-

import json
from abc import ABC, abstractmethod
from typing import Iterator, Dict

from core_aws.etls.base import IBaseEtlOnAWS


class IBaseEtlOnAwsSQS(IBaseEtlOnAWS, ABC):
    """
    Base class for ETL processes that retrieves and process the messages
    coming from a SQS queue...
    """

    def __init__(self, queue_name: str, **kwargs):
        super(IBaseEtlOnAwsSQS, self).__init__(**kwargs)
        self.queue_name = queue_name
        self.queue = None

    def pre_processing(self, **kwargs) -> None:
        self.queue = self.sqs_client.get_queue_by_name(self.queue_name)

    def _execute(self, *args, **kwargs) -> int:
        """
        It retrieves records in batches from the SQS queue and process them...
        :return: Number of processed messages.
        """

        queue_url = self.queue.url
        success_entries = []
        total = 0

        while True:
            batch = self.sqs_client.receive_messages(queue_url=queue_url, **kwargs)
            if not batch:
                break

            for message in batch:
                message_id, receipt_handle = message["MessageId"], message["ReceiptHandle"]
                self.info(f"Processing message: {message_id}...")

                # An exception in one message must not stop the execution...
                try:
                    self.process_message(message)
                    success_entries.append({"Id": message_id, "ReceiptHandle": receipt_handle})
                    total += 1

                except Exception as error:
                    self.error({
                        "MessageId": message_id,
                        "ReceiptHandle": receipt_handle,
                        "Error": error
                    })

            if success_entries:
                res = self.sqs_client.delete_messages(queue_url, success_entries)
                self.info("Below, is the output for message deletion...")
                self.info(json.dumps(res))

        return total

    @abstractmethod
    def process_message(self, message) -> Iterator[Dict]:
        """
        Process the message...

        :param message: The message to be processed.
        :return: Iterator that returns the records that message produced.
        """
