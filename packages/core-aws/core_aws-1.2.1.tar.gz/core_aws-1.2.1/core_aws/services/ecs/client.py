# -*- coding: utf-8 -*-

from typing import List, Dict

from core_aws.services.base import AwsClient
from core_aws.services.base import AwsClientException


class EcsClient(AwsClient):
    """ Client for ECS Service """

    def __init__(self, region, **kwargs):
        super().__init__("ecs", region_name=region, **kwargs)

    def list_services(self, cluster: str, **kwargs):
        """
        Returns a list of services. You can filter the results by cluster, launch
        type, and scheduling strategy...

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_services.html

        :param cluster:
            The short name or full Amazon Resource Name (ARN) of the cluster to use
            when filtering the ListServices results. If you do not specify a
            cluster, the default cluster is assumed.

        :param kwargs:
            - nextToken (string):
                The nextToken value returned from a ListServices request indicating that
                more results are available to fulfill the request and further calls will be
                needed. If maxResults was provided, it is possible the number of results
                to be fewer than maxResults .
            - maxResults (integer):
                The maximum number of service results returned by ListServices in
                paginated output. When this parameter is used, ListServices only returns
                maxResults results in a single page along with a nextToken response
                element. The remaining results of the initial request can be seen by
                sending another ListServices request with the returned nextToken
                value. This value can be between 1 and 100. If this parameter is not
                used, then ListServices returns up to 10 results and a nextToken
                value if applicable.
            - launchType (string):
                The launch type to use when filtering the ListServices results.
            - schedulingStrategy (string):
                The scheduling strategy to use when filtering the ListServices results.

        :return

            .. code-block:: python

                {
                    "serviceArns": [
                        "arn:aws:ecs:us-west-2:<account_id>:service/<cluster>/<service_name>"
                    ],
                    "ResponseMetadata": {
                        "RequestId": "da55e311-882e-4ff3-9801-23e53e1d10b5",
                        "HTTPStatusCode": 200,
                        "HTTPHeaders": {
                            "x-amzn-requestid": "da55e311-882e-4ff3-9801-23e53e1d10b5",
                            "content-type": "application/x-amz-json-1.1",
                            "content-length": "173",
                            "date": "Mon, 16 Aug 2021 14:52:24 GMT"
                        },
                        "RetryAttempts": 0
                    }
                }
            ..
        """

        try:
            return self.client.list_services(cluster=cluster, **kwargs)

        except Exception as error:
            raise AwsClientException(error)

    def describe_services(self, cluster: str, services: List, **kwargs):
        """
        Describes the specified services running in your cluster...
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_services.html

        :param cluster:
            The short name or full Amazon Resource Name (ARN) the
            cluster that hosts the service to describe. If you do not
            specify a cluster, the default cluster is assumed. This
            parameter is required if the service or services you are
            describing were launched in any cluster other than the
            default cluster.

        :param services:
            A list of services to describe. You may specify up to 10 services
            to describe in a single operation.

        :param kwargs:
            - include (list):
                Specifies whether you want to see the resource tags for the
                service. If TAGS is specified, the tags are included in the
                response. If this field is omitted, tags are not included
                in the response.
        """

        try:
            return self.client.describe_services(cluster=cluster, services=services, **kwargs)

        except Exception as error:
            raise AwsClientException(error)

    def update_service(self, service: str, **kwargs) -> Dict:
        """
        Modifies the parameters of a service. For services using the rolling
        update (ECS ) deployment controller, the desired count, deployment configuration,
        network configuration, task placement constraints and strategies, or task
        definition used can be updated...

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.update_service

        :param service: The name of the service to update.
        :param kwargs:
            - cluster (string):
                The short name or full Amazon Resource Name (ARN) of the cluster that
                your service is running on. If you do not specify a cluster, the default
                cluster is assumed.

            For the complete list check the documentation.

        :return:
        """

        try:
            return self.client.update_service(service=service, **kwargs)

        except Exception as error:
            raise AwsClientException(error)

    def list_tasks(self, **kwargs) -> Dict:
        """
        Returns a list of tasks. You can filter the results by cluster, task definition family,
        container instance, launch type, what IAM principal started the task, or by the
        desired status of the task.

        Recently stopped tasks might appear in the returned results. Currently, stopped tasks
        appear in the returned results for at least one hour.

        :param kwargs:
            - cluster (string):
                The short name or full Amazon Resource Name (ARN) of the cluster to use
                when filtering the ListTasks results. If you do not specify a
                cluster, the default cluster is assumed.
            - containerInstance (string):
                The container instance ID or full ARN of the container
                instance to use when filtering the ListTasks results. Specifying a
                containerInstance limits the results to tasks that belong to
                that container instance.
            - family (string):
                The name of the task definition family to use when filtering the ListTasks
                results. Specifying a family limits the results to tasks that
                belong to that family.
            - nextToken (string):
                The nextToken value returned from a ListTasks
                request indicating that more results are available to fulfill the
                request and further calls will be needed. If maxResults was
                provided, it is possible the number of results to be fewer than maxResults.
            - maxResults (integer):
                The maximum number of task results returned by ListTasks in paginated
                output. When this parameter is used, ListTasks only returns maxResults
                results in a single page along with a nextToken response element. The remaining
                results of the initial request can be seen by sending another ListTasks
                request with the returned nextToken value. This value can be between 1 and
                100. If this parameter is not used, then ListTasks returns up to 100 results and
                a nextToken value if applicable.
            - startedBy (string):
                The startedBy value with which to filter the task results. Specifying a
                startedBy value limits the results to tasks that were started with that value.
            - serviceName (string):
                The name of the service to use when filtering the ListTasks results. Specifying
                a serviceName limits the results to tasks that belong to that service.
            - desiredStatus (string):
                The task desired status to use when filtering the ListTasks results. Specifying a
                desiredStatus of STOPPED limits the results to tasks that Amazon ECS has set
                the desired status to STOPPED . This can be useful for debugging tasks that are
                not starting properly or have died or finished. The default status filter
                is RUNNING, which shows tasks that Amazon ECS has set the desired status to RUNNING.

        :return

            .. code-block:: python

                {
                    "taskArns": [
                        "arn:aws:ecs:us-west-2:<account_id>:task/<cluster_name>/<task_id>",
                        "arn:aws:ecs:us-west-2:<account_id>:task/<cluster_name>/<task_id>",
                    ],
                    "ResponseMetadata": {
                        "RequestId": "43ffbe9f-e5ac-4508-85ad-1bdbff476663",
                        "HTTPStatusCode": 200,
                        "HTTPHeaders": {
                            "x-amzn-requestid": "43ffbe9f-e5ac-4508-85ad-1bdbff476663",
                            "content-type": "application/x-amz-json-1.1",
                            "content-length": "620",
                            "date": "Mon, 16 Aug 2021 13:29:59 GMT"
                        },
                        "RetryAttempts": 0
                    }
                }
            ..
        """

        try:
            return self.client.list_tasks(**kwargs)

        except Exception as error:
            raise AwsClientException(error)
