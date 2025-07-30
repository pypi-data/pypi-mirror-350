# -*- coding: utf-8 -*-

from typing import Dict

from core_aws.services.base import AwsClient
from core_aws.services.base import AwsClientException


class DynamoDbClient(AwsClient):
    """ Client for DynamoDB Service """

    def __init__(self, region: str, **kwargs):
        super().__init__("dynamodb", region_name=region, **kwargs)

    def get_item(self, table: str, key: Dict, **kwargs) -> Dict:
        """
        Returns a set of attributes for the item with the given primary key. If there
        is no matching item, GetItem does not return any data and there will be
        no Item element in the response...

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_item

        :param table: The name of the table containing the requested item.
        :param key: Primary key of the item to retrieve.
        :param kwargs:

        :return: A set of attributes for the item with the given primary key.

            .. code-block:: python

                {
                    "Item": {
                        "string": {
                            "S": "string",
                            "N": "string",
                            "B": b"bytes",
                            "SS": [
                                "string",
                            ],
                            "NS": [
                                "string",
                            ],
                            "BS": [
                                b"bytes",
                            ],
                            "M": {
                                "string": {"... recursive ..."}
                            },
                            "L": [
                                {"... recursive ..."},
                            ],
                            "NULL": True|False,
                            "BOOL": True|False
                        }
                    },
                    "ConsumedCapacity": {
                        "TableName": "string",
                        "CapacityUnits": 123.0,
                        "ReadCapacityUnits": 123.0,
                        "WriteCapacityUnits": 123.0,
                        "Table": {
                            "ReadCapacityUnits": 123.0,
                            "WriteCapacityUnits": 123.0,
                            "CapacityUnits": 123.0
                        },
                        "LocalSecondaryIndexes": {
                            "string": {
                                "ReadCapacityUnits": 123.0,
                                "WriteCapacityUnits": 123.0,
                                "CapacityUnits": 123.0
                            }
                        },
                        "GlobalSecondaryIndexes": {
                            "string": {
                                "ReadCapacityUnits": 123.0,
                                "WriteCapacityUnits": 123.0,
                                "CapacityUnits": 123.0
                            }
                        }
                    }
                }
            ..
        """

        try:
            return self.client.get_item(TableName=table, Key=key, **kwargs)

        except Exception as error:
            raise AwsClientException(error)

    def update_item(
            self, table: str, key: dict, expression_attribute_values: dict,
            update_expression: str, **kwargs) -> Dict:

        """
        Edits an existing item"s attributes, or adds a new item to the table if it does not already exist.
        You can put, delete, or add attribute values. You can also perform a conditional update on an
        existing item (insert a new attribute name-value pair if it doesn"t exist, or replace an existing
        name-value pair if it has certain expected attribute values).

        You can also return the item"s attribute values in the same UpdateItem
        operation using the ReturnValues parameter...

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_item

        :param table:
        :param key:
        :param expression_attribute_values:
        :param update_expression:
        :param kwargs:

        :return:

            .. code-block:: python

                {
                    "Attributes": {
                        "string": {
                            "S": "string",
                            "N": "string",
                            "B": b"bytes",
                            "SS": [
                                "string",
                            ],
                            "NS": [
                                "string",
                            ],
                            "BS": [
                                b"bytes",
                            ],
                            "M": {
                                "string": {"... recursive ..."}
                            },
                            "L": [
                                {"... recursive ..."},
                            ],
                            "NULL": True|False,
                            "BOOL": True|False
                        }
                    },
                    "ConsumedCapacity": {
                        "TableName": "string",
                        "CapacityUnits": 123.0,
                        "ReadCapacityUnits": 123.0,
                        "WriteCapacityUnits": 123.0,
                        "Table": {
                            "ReadCapacityUnits": 123.0,
                            "WriteCapacityUnits": 123.0,
                            "CapacityUnits": 123.0
                        },
                        "LocalSecondaryIndexes": {
                            "string": {
                                "ReadCapacityUnits": 123.0,
                                "WriteCapacityUnits": 123.0,
                                "CapacityUnits": 123.0
                            }
                        },
                        "GlobalSecondaryIndexes": {
                            "string": {
                                "ReadCapacityUnits": 123.0,
                                "WriteCapacityUnits": 123.0,
                                "CapacityUnits": 123.0
                            }
                        }
                    },
                    "ItemCollectionMetrics": {
                        "ItemCollectionKey": {
                            "string": {
                                "S": "string",
                                "N": "string",
                                "B": b"bytes",
                                "SS": [
                                    "string",
                                ],
                                "NS": [
                                    "string",
                                ],
                                "BS": [
                                    b"bytes",
                                ],
                                "M": {
                                    "string": {"... recursive ..."}
                                },
                                "L": [
                                    {"... recursive ..."},
                                ],
                                "NULL": True|False,
                                "BOOL": True|False
                            }
                        },
                        "SizeEstimateRangeGB": [
                            123.0,
                        ]
                    }
                }
            ..
        """

        try:
            return self.client.update_item(
                TableName=table, Key=key,
                ExpressionAttributeValues=expression_attribute_values,
                UpdateExpression=update_expression,
                **kwargs
            )

        except Exception as error:
            raise AwsClientException(error)
