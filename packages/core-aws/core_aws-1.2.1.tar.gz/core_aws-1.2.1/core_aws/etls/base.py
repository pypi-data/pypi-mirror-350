# -*- coding: utf-8 -*-

import json
from abc import ABC
from contextlib import suppress
from typing import List, Dict

from core_etl.base import IBaseETL

from core_aws.services.s3.client import S3Client
from core_aws.services.sqs.client import SqsClient
from core_aws.services.ssm.client import SsmClient


class IBaseEtlOnAWS(IBaseETL, ABC):
    """
    Base class for ETL tasks executed on AWS. It provides common features
    can be used into the ETL processes...
    """

    def __init__(
            self, aws_region: str = None, ssm_parameters_path: str = None,
            attrs_to_update: List[str] = None, json_attrs: List[str] = None,
            ssm_endpoint_url: str = None, **kwargs):

        """
        :param aws_region: AWS Region.
        :param ssm_parameters_path: Path under we can find the parameters to use.
        :param attrs_to_update: List of attributes to update (on the object) from SSM parameters.
        :param json_attrs: Attributes should be loaded as json (dicts, list).
        :param ssm_endpoint_url: Private URL to connect to SSM service.
        """

        super(IBaseEtlOnAWS, self).__init__(**kwargs)

        self.aws_region = aws_region
        self.ssm_parameters_path = ssm_parameters_path
        self.attrs_to_update = attrs_to_update or []
        self.json_attrs = json_attrs or []

        # Some useful clients to have. We could add more if required...
        ssm_args = {"endpoint_url": ssm_endpoint_url} if ssm_endpoint_url else {}

        self.ssm_client = SsmClient(region=self.aws_region, **ssm_args)
        self.sqs_client = SqsClient(region=self.aws_region)
        self.s3_client = S3Client()

    def pre_processing(self, **kwargs) -> None:
        """ It updates the attributes and parse the json attributes """

        super(IBaseEtlOnAWS, self).pre_processing(**kwargs)
        self._update_parameters(self.attrs_to_update)

        for attr in self.json_attrs:
            value = getattr(self, attr)
            if value:
                with suppress(Exception):
                    setattr(self, attr, json.loads(value))

    def _update_parameters(self, attrs: List[str]) -> None:
        """
        It retrieves the parameters from SSM Parameter Store service
        and update the object's attributes...
        """

        if self.ssm_parameters_path:
            self.info("Getting attributes from SSM Parameter Store service...")
            params = list(self.ssm_client.get_parameters_by_path(self.ssm_parameters_path))
            self._update_attributes(attributes=attrs, parameters=params)
            self.info("The attributes were updated!")

    def _update_attributes(self, attributes: List[str], parameters: List[Dict]) -> None:
        """
        It updates the object (self) attributes using the values in the parameters
        coming from SSM Parameter Store service...

        :param attributes: Attribute list.
        :param parameters: Parameters values.

        Example...

            Using the following...

                .. code-block:: python

                    [{
                        "Name": "/path/service/user",
                        "Value": "user_name"
                    }]
                ..

            For an object that contains a "user" attribute with the
            value: "/path/service/user", the attribute (user) will be updated
            with value: "user_name".
        """

        for attr in attributes:
            current_val = getattr(self, attr, False)
            if current_val:
                for parameter in parameters:
                    if parameter.get("Name") == current_val:
                        setattr(self, attr, parameter.get("Value", None))
