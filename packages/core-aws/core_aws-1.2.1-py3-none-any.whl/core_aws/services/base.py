# -*- coding: utf-8 -*-

import boto3


class AwsClient:
    """ Base class for all AWS Service's clients """

    def __init__(self, service: str, **kwargs):
        self.client = boto3.client(service, **kwargs)


class AwsClientException(Exception):
    """ Custom exception for AwsClients """
