# -*- coding: utf-8 -*-

from typing import Dict, List, Iterator

from boto3 import resource
from botocore.exceptions import ClientError
from core_mixins.utils import get_batches

from core_aws.services.base import AwsClient
from core_aws.services.base import AwsClientException


class SqsClient(AwsClient):
    """ Client for SQS Service """

    def __init__(self, region, **kwargs):
        super().__init__("sqs", region_name=region, **kwargs)
        self.resource = resource("sqs")

    def get_queue_by_name(self, queue_name: str, **kwargs) -> "boto3.resources.factory.sqs.Queue":
        """
        It returns the Queue of an existing Amazon SQS queue...

        To access a queue that belongs to another AWS account, use the QueueOwnerAWSAccountId
        parameter to specify the account ID of the queue’s owner. The queue’s owner must grant you
        permission to access the queue...

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/service-resource/get_queue_by_name.html

        :param queue_name: The name of the queue.
        :param kwargs:
            * QueueOwnerAWSAccountId: The Amazon Web Services account ID of the account that created the queue.

        :return: It returns a sqs.Queue object that contains the below attributes:
            - url: https://sqs.<region>.amazonaws.com/<account>/QueueName
            - dead_letter_source_queues: DLQ info.
            - meta: Info.
            - attributes: It's a dictionary

                .. code-block:: python

                    {
                        'QueueArn': 'arn:aws:sqs:...',
                        'ApproximateNumberOfMessages': '0',
                        'ApproximateNumberOfMessagesNotVisible': '0',
                        'ApproximateNumberOfMessagesDelayed': '0',
                        'CreatedTimestamp': '1699539978',
                        'LastModifiedTimestamp': '1699540164',
                        'VisibilityTimeout': '300',
                        'MaximumMessageSize': '262144',
                        'MessageRetentionPeriod': '3600',
                        'DelaySeconds': '60',
                        ...
                    }
                ..
        """

        return self.resource.get_queue_by_name(QueueName=queue_name, **kwargs)

    def send_message(self, queue_url: str, message: str, **kwargs):
        """
        Delivers a message to the specified queue. A message can include
        only XML, JSON, and no formatted text. The following Unicode characters
        are allowed:

        ***************************************************************************
         #x9 | #xA | #xD | #x20 to #xD7FF | #xE000 to #xFFFD | #x10000 to #x10FFFF
        ***************************************************************************

        More info:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message
        """

        try:
            return self.client.send_message(
                QueueUrl=queue_url,
                MessageBody=message,
                **kwargs)

        except ClientError as error:
            raise AwsClientException(error)

    def send_message_batch(self, queue_url: str, entries: List[Dict], **kwargs):
        """
        Delivers up to ten messages to the specified queue. This is a batch
        version of "send_message". For a FIFO queue, multiple messages within a
        single batch are enqueued in the order they are sent...

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/client/send_message_batch.html
        """

        try:
            return self.client.send_message_batch(
                QueueUrl=queue_url,
                Entries=entries,
                **kwargs)

        except ClientError as error:
            raise AwsClientException(error)

    def receive_messages(self, queue_url: str, max_number_of_msg: int = 10, **kwargs) -> List[Dict]:
        """
        Retrieves one or more messages (up to 10), from the specified
        queue. Using the WaitTimeSeconds parameter enables long-poll
        support. For more information, see Amazon SQS Long Polling in
        the Amazon SQS Developer Guide...

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/client/receive_message.html

        :return: List of dictionaries with the following structure.

            .. code-block:: python

                {
                    "MessageId": "string",
                    "ReceiptHandle": "string",
                    "MD5OfBody": "string",
                    "Body": "string",
                    "Attributes": {
                        "string": "string"
                    },
                    "MD5OfMessageAttributes": "string",
                    "MessageAttributes": {
                        "string": {
                            "StringValue": "string",
                            "BinaryValue": b"bytes",
                            "StringListValues": [
                                "string",
                            ],
                            "BinaryListValues": [
                                b"bytes",
                            ],
                            "DataType": "string"
                        }
                    }
                }
            ..
        """

        try:
            return self.client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_number_of_msg,
                **kwargs).get("Messages", [])

        except ClientError as error:
            raise AwsClientException(error)

    def retrieve_all_messages(self, queue_url: str, **kwargs) -> Iterator[Dict]:
        """ Custom method that retrieves all the messages in the queue through the iterator """

        while True:
            messages = self.receive_messages(queue_url=queue_url, **kwargs)
            if not messages:
                break

            yield from messages

    def delete_message(self, queue_url: str, receipt_handle: str, **kwargs) -> None:
        """
        Deletes the specified message from the specified queue. To select the
        message to delete, use the ReceiptHandle of the message (not the MessageId
        which you receive when you send the message). Amazon SQS can delete a
        message from a queue even if a visibility timeout setting causes the message
        to be locked by another consumer. Amazon SQS automatically deletes messages
        left in a queue longer than the retention period configured for the queue.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/client/delete_message.html
        """

        try:
            return self.client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle,
                **kwargs)

        except ClientError as error:
            raise AwsClientException(error)

    def delete_message_batch(self, queue_url: str, entries: List[Dict[str, str]], **kwargs) -> Dict:
        """
        Deletes the specified message from the specified queue. To select the
        message to delete, use the ReceiptHandle of the message (not the MessageId
        which you receive when you send the message). Amazon SQS can delete a
        message from a queue even if a visibility timeout setting causes the message
        to be locked by another consumer. Amazon SQS automatically deletes messages
        left in a queue longer than the retention period configured for the queue.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/client/delete_message_batch.html

        :return:
            .. code-block:: python

                {
                    "Successful": [
                        {
                            "Id": "string"
                        },
                    ],
                    "Failed": [
                        {
                            "Id": "string",
                            "SenderFault": True|False,
                            "Code": "string",
                            "Message": "string"
                        },
                    ]
                }
            ..
        """

        try:
            return self.client.delete_message_batch(
                QueueUrl=queue_url,
                Entries=entries,
                **kwargs)

        except ClientError as error:
            raise AwsClientException(error)

    def delete_messages(
            self, queue_url: str, entries: List[Dict[str, str]],
            retries: int = 3, **kwargs) -> Dict:

        """
        It's a wrapper over "delete_message_batch" and will delete all messages, if a
        message deletion fails it will be re-tried until success or until the
        maximum attempts are exhausted...

        :param queue_url: The SQS queue url.
        :param entries: The messages reference to delete.
        :param retries: Number of re-tries in case of errors while deleting the messages.
        :param kwargs: Other arguments to pass to delete_message_batch method.

        :return:

            .. code-block:: python

                {
                    "Successful": [{
                        "Id": "string"
                    }],
                    "Failed": [{
                        "Id": "string",
                        "SenderFault": True|False,
                        "Code": "string",
                        "Message": "string"
                    }]
                }
            ..
        """

        successful = []

        def _delete_batch(messages: List[Dict]) -> List[Dict]:
            failures_: List[Dict] = []

            for batch_ in get_batches(messages, 10):
                output = self.delete_message_batch(
                    queue_url=queue_url,
                    entries=batch_,
                    **kwargs)

                successful.extend(output.get("Successful", []))
                failures_.extend(output.get("Failed", []))

            return failures_

        failed = [rec["Id"] for rec in _delete_batch(entries)]
        entries = [record for record in entries if record["Id"] in failed]
        failures = []

        while entries and retries:
            failures = _delete_batch(entries)
            failures_ids = [rec["Id"] for rec in failures]
            entries = [record for record in entries if record["Id"] in failures_ids]
            retries -= 1

        return {
            "Successful": successful,
            "Failed": failures
        }
