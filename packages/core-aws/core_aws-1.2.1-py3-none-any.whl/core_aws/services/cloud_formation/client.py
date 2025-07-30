# -*- coding: utf-8 -*-

from typing import Dict

from core_aws.services.base import AwsClient


class CloudFormationClient(AwsClient):
    """ Client for CloudFormation Service """

    def __init__(self, region: str, **kwargs):
        super().__init__("cloudformation", region_name=region, **kwargs)

    def describe_stack(self, stack_name: str) -> Dict:
        return self.client.describe_stacks(StackName=stack_name)["Stacks"][0]

    def get_output_value(self, stack_name: str, export_name: str):
        for output in self.describe_stack(stack_name)["Outputs"]:
            if output.get("ExportName") == export_name:
                return output["OutputValue"]

        return None
