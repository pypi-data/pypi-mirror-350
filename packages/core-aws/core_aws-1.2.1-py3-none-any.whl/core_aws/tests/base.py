# -*- coding: utf-8 -*-

from typing import Dict
from unittest.mock import patch

import botocore.session

from core_tests.tests.base import BaseTestCase

from core_aws.typing.client_context import ClientContext
from core_aws.typing.cognito_identity import CognitoIdentity
from core_aws.typing.lambda_context import LambdaContext
from core_aws.typing.mobile_client import MobileClient


class BaseAwsTestCase(BaseTestCase):
    """ Base class for Test Cases related to AWS and boto3 """

    aws_patcher = patch("botocore.client.BaseClient._make_api_call")
    aws_client_mock = None

    @classmethod
    def setUpClass(cls) -> None:
        super(BaseAwsTestCase, cls).setUpClass()
        cls.aws_client_mock = cls.aws_patcher.start()
        cls.aws_client_mock.side_effect = cls._make_api_call

    @classmethod
    def tearDownClass(cls) -> None:
        super(BaseAwsTestCase, cls).tearDownClass()
        cls.aws_patcher.stop()

    @staticmethod
    def _make_api_call(operation_name, api_params):
        """ Each class should implement the response """

    @staticmethod
    def sample_context():
        return LambdaContext(
            function_name="Lambda-Function-Name",
            function_version="$LATEST",
            invoked_function_arn="arn:aws:lambda:us-east-1:******:function:Lambda-Function-Name",
            memory_limit_in_mb=128,
            aws_request_id="65e839d8-650a-4803-8c08-1d7fcc62cc5e",
            log_group_name="/aws/lambda/Lambda-Function-Name",
            log_stream_name="2021/05/03/[$LATEST]34cc5b8a888241b383ff071d82520797",
            identity=CognitoIdentity(
                cognito_identity_id="some-id",
                cognito_identity_pool_id="some-pool-id"
            ),
            client_context=ClientContext(
                client=MobileClient(
                    installation_id="some-inst-id",
                    app_title="Some-App",
                    app_version_name="some-version",
                    app_version_code="x01zT",
                    app_package_name="app-pkg"
                ),
                custom={},
                env={}
            )
        )

    @staticmethod
    def sample_event_from_queue():
        return {
            "Records": [
                {
                    "messageId": "ae76a2d9-2064-40df-8dff-6aa9c3d10005",
                    "receiptHandle": "AQEBP2si5WM8TgtuepI7mN+YJqIwm8Fermi7mEELXoLBFMFiEel9j+",
                    "body": '{"value": 1}',
                    "attributes": {
                        "ApproximateReceiveCount": "2",
                        "SentTimestamp": "1699540922291",
                        "SenderId": "AROATQUBASLD2M2Y6MM3A:******",
                        "ApproximateFirstReceiveTimestamp": "1699540982292"
                    },
                    "messageAttributes": {},
                    "md5OfMessageAttributes": None,
                    'md5OfBody': "1ff00094a5ba112cb7dd128e783d6803",
                    "eventSource": "aws:sqs",
                    "eventSourceARN": "arn:aws:sqs:us-east-1:******:SampleQueue",
                    "awsRegion": "us-east-1"
                },
                {
                    "messageId": "fd45b65d-b44f-4e91-b8bd-778f8ddb1601",
                    "receiptHandle": "AQEB6Cnrp7qHg1fNCT12vt6N8hg85s6HQJcc2KOZ50qG6LJQZ+",
                    "body": '{"value":2}',
                    "attributes": {
                        "ApproximateReceiveCount": "2",
                        "SentTimestamp": "1699540928208",
                        "SenderId": "AROATQUBASLD2M2Y6MM3A:******",
                        "ApproximateFirstReceiveTimestamp": "1699540988209"
                    }, "messageAttributes": {},
                    "md5OfMessageAttributes": None,
                    "md5OfBody": "5d872de403edb944a7b10450eda2f46a",
                    "eventSource": "aws:sqs",
                    "eventSourceARN": "arn:aws:sqs:us-east-1:******:SampleQueue",
                    "awsRegion": "us-east-1"
                }
            ]
        }

    @staticmethod
    def sample_event_from_topic():
        return {
            "Records": [{
                "EventSource": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:us-east-1:******:SampleTopic:b7cfd752-05a9-4155-a1eb-6c9552a50d5b",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "33089596-71cb-5270-926e-c8516313cfc8",
                    "TopicArn": "arn:aws:sns:us-east-1:******:SampleTopic",
                    "Subject": None,
                    "Message": '{"value": 1}',
                    "Timestamp": "2023-11-09T17:02:16.286Z",
                    "SignatureVersion": "1",
                    "Signature": "QKgmQUcfzypgriomDr7NuUzQV==",
                    "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-******.pem",
                    "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:******:SampleTopic:b7cfd752-05a9-4155-a1eb-6c9552a50d5b",
                    "MessageAttributes": {}
                }
            }]
        }

    @staticmethod
    def sample_event_from_kinesis_data_string():
        return {
            "Records": [{
                "kinesis": {
                    "kinesisSchemaVersion": "1.0",
                    "partitionKey": "binlog",
                    "sequenceNumber": "49647175778160097793486557372840800878012000746547970050",
                    "data": "eyJldmVudF90aW1lc3RhbXAiOiAxNzAxNDY4MjkwLCAiZXZlbnRfdHlwZSI6ICJJTlNFUlQiLCAiZ3RpZCI6IG51bGwsICJzZXJ2aWNlIjogImJpbmxvZy1wcm9jZXNzb3IiLCAic291cmNlIjogImJpbmxvZy4wMDAwMDEiLCAicG9zaXRpb24iOiAxOTA0LCAicHJpbWFyeV9rZXkiOiAicGVyc29uX2lkIiwgInNjaGVtYV9uYW1lIjogInNvdXJjZSIsICJ0YWJsZV9uYW1lIjogInBlcnNvbiIsICJhdHRycyI6IHsicGVyc29uX2lkIjogMSwgImZpcnN0X25hbWUiOiAiSm9obiIsICJsYXN0X25hbWUiOiAiRG9lIiwgImRhdGVfb2ZfYmlydGgiOiAiMTk5MC0wMS0xNSIsICJlbWFpbCI6ICJqb2huLmRvZUBlbWFpbC5jb20iLCAiYWRkcmVzcyI6ICIxMjMgTWFpbiBTdCIsICJjcmVhdGVkX29uIjogIjIwMjMtMTItMDFUMjI6MDQ6NTAiLCAidXBkYXRlZF9vbiI6ICIyMDIzLTEyLTAxVDIyOjA0OjUwIn19",
                    "approximateArrivalTimestamp": 1702071427.66
                },
                "eventSource": "aws:kinesis",
                "eventVersion": "1.0",
                "eventID": "shardId-000000000000:49647175778160097793486557372840800878012000746547970050",
                "eventName": "aws:kinesis:record",
                "invokeIdentityArn": "arn:aws:iam::******:role/service-role/test-role",
                "awsRegion": "us-east-1",
                "eventSourceARN": "arn:aws:kinesis:us-east-1:******:stream/test"
            }]
        }

    @staticmethod
    def generate_error(
            service: str = "ssm", region_name: str = "us-east-1",
            operation_name="GetParameter", error_response: Dict = None):

        """
        It generates an error like the one generated by botocore. By default, and
        as an example generating ParameterNotFound error.
        """

        error_response = error_response or {
                "Error": {
                    "Code": "ParameterNotFound",
                    "Message": "The parameter was not found."
                }
            }

        return botocore.session.get_session() \
            .create_client(
                service_name=service,
                region_name=region_name
            ) \
            .exceptions.ParameterNotFound(
                error_response=error_response,
                operation_name=operation_name
            )
