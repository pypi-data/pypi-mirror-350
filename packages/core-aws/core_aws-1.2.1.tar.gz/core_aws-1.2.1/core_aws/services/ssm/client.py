# -*- coding: utf-8 -*-

import inspect
from typing import List, Dict, Iterator

from core_aws.services.base import AwsClient
from core_aws.services.base import AwsClientException


class SsmClient(AwsClient):
    """ Client for SSM Service """

    def __init__(self, region, **kwargs):
        super().__init__("ssm", region_name=region, **kwargs)

    def get_secret(self, secret_id: str):
        """
        It returns the secret from Secrets Manager service given the id...

        :param secret_id: The ID of the secret.
        :return: The value of the secret.
        """

        try:
            return self.get_parameter(
                parameter_name=f"/aws/reference/secretsmanager/{secret_id}",
                with_decryption=True)["Value"]

        except Exception as error:
            raise AwsClientException(error)

    def get_parameter(self, parameter_name, with_decryption=True) -> Dict:
        """
        Get information about a parameter by using the parameter name...
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameter.html

        :param parameter_name: The name of the parameter you want to query.

        :param with_decryption:
            Returns decrypted values for secure string parameters. This flag is ignored
            for String and StringList parameter types.

        :return:

            .. code-block:: python

                {
                    "Name": "string",
                    "Type": "String"|"StringList"|"SecureString",
                    "Value": "string",
                    "Version": 123,
                    "Selector": "string",
                    "SourceResult": "string",
                    "LastModifiedDate": datetime(2015, 1, 1),
                    "ARN": "string",
                    "DataType": "string"
                }
            ..
        """

        try:
            response = self.client.get_parameter(
                Name=parameter_name,
                WithDecryption=with_decryption)

            return response["Parameter"]

        except Exception as error:
            raise AwsClientException(error)

    def get_parameters_by_path(self, path: str, with_decryption=True, **kwargs) -> Iterator[Dict]:
        """
        Retrieve the parameters under a specific path...
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameters_by_path.html

        :param path: Path -- The hierarchy for the parameter. Hierarchies start with a forward slash (/) and end with the
                     parameter name. A parameter name hierarchy can have a maximum of 15 levels. Here is an example
                     of a hierarchy: `/key_`...

        :param with_decryption: WithDecryption (boolean)
            - Retrieve all parameters in a hierarchy with their value decrypted.

        :param kwargs:
            - Recursive (boolean) -- (Retrieve all parameters within a hierarchy)

            - ParameterFilters
                (list) -- Filters to limit the request results.
                (dict) -- One or more filters. Use a filter to return a more specific list of results.

            - MaxResults (integer) --
                The maximum number of items to return for this call.
                The call also returns a token that you can specify in a subsequent
                call to get the next set of results.

            - NextToken (string) -- A token to start the list. Use this token to get the next set of results.

        :return: Iterator with the parameters with the structure.

            .. code-block:: python

                {
                    "Name": "string",
                    "Type": "String"|"StringList"|"SecureString",
                    "Value": "string",
                    "Version": 123,
                    "Selector": "string",
                    "SourceResult": "string",
                    "LastModifiedDate": datetime(2015, 1, 1),
                    "ARN": "string",
                    "DataType": "string"
                }
            ..
        """

        try:
            while True:
                response = self.client.get_parameters_by_path(
                    Path=path,
                    WithDecryption=with_decryption,
                    **kwargs)

                yield from response.get("Parameters", [])
                next_token = response.get("NextToken")
                if not next_token:
                    return

                kwargs["NextToken"] = next_token

        except Exception as error:
            raise AwsClientException(error)

    def put_parameter(self, name: str, value: str, overwrite: bool = False, **kwargs) -> Dict:
        """
        Add or update a parameter...
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.put_parameter

        :param name:
            The fully qualified name of the parameter that you want to add
            to the system. The fully qualified name includes the complete
            hierarchy of the parameter path and name. For parameters in a
            hierarchy, you must include a leading forward slash character (/)
            when you create or reference a parameter.
            For example: /Dev/DBServer/MySQL/db-string13

        :param value:
            The parameter value that you want to add to the system. Standard
            parameters have a value limit of 4 KB. Advanced parameters have
            a value limit of 8 KB.

        :param overwrite: Overwrite an existing parameter. The default value is false.

        :param kwargs:
            - Description: (string)
                Information about the parameter that you want to add to
                the system. Optional but recommended.

            - Type: (string)
                The type of parameter that you want to add to the system.
                <String | StringList | SecureString>

            - KeyId: (string)
                The Key Management Service (KMS) ID that you want to use to
                encrypt a parameter. Either the default KMS key automatically
                assigned to your Amazon Web Services account or a custom
                key. Required for parameters that use the SecureString data type.

                If you don"t specify a key ID, the system uses the default key
                associated with your Amazon Web Services account.

            - AllowedPattern: (string)
                A regular expression used to validate the parameter
                value. For example, for String types with values restricted
                to numbers, you can specify the following: AllowedPattern=^d+$

            - Tags: (list)
                Optional metadata that you assign to a resource. Tags enable
                you to categorize a resource in different ways, such as
                by purpose, owner, or environment. For example, you might want
                to tag a Systems Manager parameter to identify the type of
                resource to which it applies, the environment, or the type
                of configuration data referenced by the parameter. In this case,
                you could specify the following key-value pairs:

                .. code-block:: text

                    Key=Resource,Value=S3bucket
                    Key=OS,Value=Windows
                    Key=ParameterType,Value=LicenseKey
                ..

            - Tier: (string)
                The parameter tier to assign to a parameter. Parameter Store
                offers a standard tier and an advanced tier for parameters.

                Standard parameters have a content size limit of 4 KB and
                can"t be configured to use parameter policies. You can create
                a maximum of 10,000 standard parameters for each Region in
                an Amazon Web Services account. Standard parameters are offered
                at no additional cost.

        :return:

            .. code-block:: python

                {
                    "Version": 123,
                    "Tier": "Standard" | "Advanced" | "Intelligent-Tiering"
                }
            ..
        """

        try:
            return self.client.put_parameter(
                Name=name, Value=value,
                Overwrite=overwrite,
                **kwargs)

        except Exception as error:
            raise AwsClientException(error)

    def retrieve_parameters_from_ssm(self, ssm_path: str, parameters: List[str]) -> Dict[str, str]:
        """
        Retrieve and return a dictionary with the parameters specified. The parameters
        will be extracted using the suffix...

        :param ssm_path: SSM Path to extract the parameters.
        :param parameters: List of suffix to extract.
        :return: Dictionary with the values.
        """

        results = {}
        for attr in parameters:
            for credential in self.get_parameters_by_path(ssm_path):
                if credential.get("Name", "").endswith(attr):
                    results[attr] = credential.get("Value", "")

        return results

    def update_obj_attrs(self, obj: object, ssm_path: str) -> None:
        """ Replace the value of the object's attrs with those retrieved from SSM """

        for credential in self.get_parameters_by_path(ssm_path):
            for name, value in inspect.getmembers(obj):
                if not name.startswith("_") and not inspect.ismethod(value):
                    if credential.get("Name", "") == value:
                        setattr(obj, name, credential.get("Value"))
