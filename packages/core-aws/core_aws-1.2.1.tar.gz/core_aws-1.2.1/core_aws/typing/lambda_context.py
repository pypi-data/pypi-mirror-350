# -*- coding: utf-8 -*-

from .client_context import ClientContext
from .cognito_identity import CognitoIdentity


class LambdaContext:
    """
    It provides methods and properties that provide information
    about the invocation, function, and execution environment.
    """

    def __init__(
            self, function_name: str, function_version: str, invoked_function_arn: str,
            memory_limit_in_mb: int, aws_request_id: str, log_group_name: str,
            log_stream_name: str, identity: CognitoIdentity,
            client_context: ClientContext) -> None:

        """
        :param function_name: The name of the Lambda function.
        :param function_version: The version of the function.

        :param invoked_function_arn:
            The Amazon Resource Name (ARN) that's used to invoke the function. Indicates if
            the invoker specified a version number or alias.

        :param memory_limit_in_mb: The amount of memory that's allocated for the function.
        :param aws_request_id: The identifier of the invocation request.
        :param log_group_name: The log group for the function.
        :param log_stream_name: The log stream for the function instance.

        :param identity: Information about the Amazon Cognito identity that authorized the request. (mobile apps)
        :param client_context: Client context that's provided to Lambda by the client application. (mobile apps)
        """

        self._function_name = function_name
        self._function_version = function_version
        self._invoked_function_arn = invoked_function_arn

        self._memory_limit_in_mb = memory_limit_in_mb
        self._aws_request_id = aws_request_id

        self._log_group_name = log_group_name
        self._log_stream_name = log_stream_name

        self._identity = identity
        self._client_context = client_context

    @property
    def function_name(self) -> str:
        return self._function_name

    @property
    def function_version(self) -> str:
        return self._function_version

    @property
    def invoked_function_arn(self) -> str:
        return self._invoked_function_arn

    @property
    def aws_request_id(self) -> str:
        return self._aws_request_id

    @property
    def memory_limit_in_mb(self) -> int:
        return self._memory_limit_in_mb

    @property
    def log_group_name(self) -> str:
        return self._log_group_name

    @property
    def log_stream_name(self) -> str:
        return self._log_stream_name

    @property
    def identity(self) -> CognitoIdentity:
        return self._identity

    @property
    def client_context(self) -> ClientContext:
        return self._client_context

    @staticmethod
    def get_remaining_time_in_millis() -> int:
        """ It returns the milliseconds left before the execution times out """
