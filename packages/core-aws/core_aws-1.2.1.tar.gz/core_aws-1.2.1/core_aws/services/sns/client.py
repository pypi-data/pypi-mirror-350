# -*- coding: utf-8 -*-

from __future__ import annotations

import json
from collections import defaultdict
from typing import Dict, Optional
from typing import List

from boto3 import resource
from botocore.exceptions import ClientError
from core_mixins.utils import get_batches

from core_aws.services.base import AwsClient
from core_aws.services.base import AwsClientException


class SnsMessage:
    """ Message that will be sent to a topic """

    # noinspection PyPep8Naming
    def __init__(
            self, Message: Dict | str, Id: str = None,
            Subject: Optional[str] = None, MessageStructure: Optional[str] = None,
            MessageAttributes: Optional[Dict] = None, MessageDeduplicationId: Optional[str] = None,
            MessageGroupId: Optional[str] = None) -> None:

        """
        :param Id:
            An identifier for the message in a batch. This attribute will be only used
            with publish_batch operation.

        :param Message:
            The message you want to send. If you are publishing to a topic and you want to
            send the same message to all transport protocols, include the text of the message
            as a String value. If you want to send different messages for each transport
            protocol, set the value of the MessageStructure parameter to json and use
            a JSON object for the Message parameter.

            Constraints:
                * Except for SMS, messages must be UTF-8 encoded strings and
                at most 256 KB in size (262,144 bytes, not 262,144 characters).

                * For SMS, each message can contain up to 140 characters. This character limit
                depends on the encoding schema. For example, an SMS message can contain 160 GSM characters,
                140 ASCII characters, or 70 UCS-2 characters. If you publish a message that exceeds this
                size limit, Amazon SNS sends the message as multiple messages, each fitting within the
                size limit. Messages aren’t truncated mid-word but are cut off at whole-word
                boundaries. The total size limit for a single SMS Publish action
                is 1,600 characters.

        :param Subject:
            Optional parameter to be used as the “Subject” line when the message is delivered to
            email endpoints. This field will also be included, if present, in the standard JSON messages
            delivered to other endpoints.

        :param MessageStructure:
            Set MessageStructure to json if you want to send a different message for each
            protocol. For example, using one publish action, you can send a short message to
            your SMS subscribers and a longer message to your email subscribers. If you
            set MessageStructure to json, the value of the Message parameter must:
                * be a syntactically valid JSON object; and
                * contain at least a top-level JSON key of “default” with a value that is a string.

            You can define other top-level keys that define the message you want to send
            to a specific transport protocol (e.g., “http”).

        :param MessageAttributes: Message attributes for "publish" action.

        :param MessageDeduplicationId:
            This parameter applies only to FIFO (first-in-first-out) topics. The MessageDeduplicationId
            can contain up to 128 alphanumeric characters (a-z, A-Z, 0-9) and
            punctuation (!"#$%&'()*+,-./:;<=>?@[]^_`{|}~).

            Every message must have a unique MessageDeduplicationId, which is a token used for
            deduplication of sent messages. If a message with a particular MessageDeduplicationId is sent
            successfully, any message sent with the same MessageDeduplicationId during the 5-minute
            deduplication interval is treated as a duplicate.

            If the topic has ContentBasedDeduplication set, the system generates a MessageDeduplicationId
            based on the contents of the message. Your MessageDeduplicationId
            overrides the generated one.

        :param MessageGroupId:
            This parameter applies only to FIFO (first-in-first-out) topics. The MessageGroupId can
            contain up to 128 alphanumeric characters (a-z, A-Z, 0-9) and
            punctuation (!"#$%&'()*+,-./:;<=>?@[]^_`{|}~).

            The MessageGroupId is a tag that specifies that a message belongs to a specific message
            group. Messages that belong to the same message group are processed in a FIFO
            manner (however, messages in different message groups might be processed
            out of order). Every message must include a MessageGroupId.
        """

        self.Id = Id
        self.Message = Message
        self.Subject = Subject

        self.MessageStructure = MessageStructure
        self.MessageAttributes = MessageAttributes
        self.MessageDeduplicationId = MessageDeduplicationId
        self.MessageGroupId = MessageGroupId

    def as_dict(self) -> Dict:
        """ It returns the required payload to be sent to the SNS topic """

        res = {
            "Id": self.Id,
            "Message": self.Message,
            "Subject": self.Subject,
            "MessageStructure": self.MessageStructure,
            "MessageAttributes": self.MessageAttributes,
            "MessageDeduplicationId": self.MessageDeduplicationId,
            "MessageGroupId": self.MessageGroupId
        }

        if type(self.Message) is dict:
            res["MessageStructure"] = "json"
            res["Message"] = json.dumps({"default": json.dumps(self.Message)})

        for key, value in list(res.items()):
            if not value:
                del res[key]

        return res


class SnsClient(AwsClient):
    """ Client for SNS Service """

    def __init__(self, region, batch_size: int = 10, **kwargs):
        super().__init__("sns", region_name=region, **kwargs)

        self.resource = resource("sns")
        self.batch_size = batch_size

    def publish_message(
            self, message: SnsMessage, topic_arn: str = None, target_arn: str = None,
            phone_number: str = None) -> Dict:

        """
        It sends a message to an Amazon SNS topic, a text message (SMS message) directly
        to a phone number, or a message to a mobile platform endpoint (when you
        specify the TargetArn)...

        :param message: The message to send to the SNS topic, target or phone...

        :param topic_arn:
            The topic you want to publish to. If you don’t specify a value for the TopicArn
            parameter, you must specify a value for the PhoneNumber
            or TargetArn parameters.

        :param target_arn:
            If you don’t specify a value for the TargetArn parameter, you must specify a value
            for the PhoneNumber or TopicArn parameters.

        :param phone_number:
            The phone number to which you want to deliver an SMS message. Use E.164
            format. If you don’t specify a value for the PhoneNumber parameter, you must
            specify a value for the TargetArn or TopicArn parameters.

        More boto3 information...
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/client/publish.html

        :return: A dict that contains:
            * MessageId: Unique identifier (string) assigned to the published message.
            * SequenceNumber: This response element applies only to FIFO (first-in-first-out) topics.
        """
        
        if not any([topic_arn, target_arn, phone_number]):
            raise AwsClientException(
                "You need to specify at one of the following arguments: topic_arn, target_arn, phone_number!"
            )

        message.Id = None
        kwargs = message.as_dict()

        for key, value in (("TargetArn", target_arn), ("TopicArn", topic_arn), ("PhoneNumber", phone_number)):
            if value:
                kwargs[key] = value
        
        try:
            return self.client.publish(**kwargs)

        except ClientError as error:
            raise AwsClientException(error)

    def publish_batch(self, topic_arn: str, messages: List[SnsMessage]) -> Dict:
        """
        Publishes up to ten messages to the specified topic. This is a batch version
        of Publish. For FIFO topics, multiple messages within a single batch are published in
        the order they are sent, and messages are deduplicated within the batch and
        across batches for 5 minutes.

        :param topic_arn: The topic you want to publish to.
        :param messages: Messages to send to the topic...

        More boto3 information...
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/client/publish_batch.html

        :return: A dict that contains:

            .. code-block:: python

                {
                    "Successful": [
                        {
                            "Id": "string",
                            "MessageId": "string",
                            "SequenceNumber": "string"
                        },
                    ],
                    "Failed": [
                        {
                            "Id": "string",
                            "Code": "string",
                            "Message": "string",
                            "SenderFault": True | False
                        },
                    ]
                }
            ..
        """

        result = defaultdict(list)

        for batch in get_batches(messages, self.batch_size):
            response = self.client.publish_batch(
                TopicArn=topic_arn,
                PublishBatchRequestEntries=[x.as_dict() for x in batch])

            for key, value in response.items():
                result[key].extend(value)

        return dict(result)
