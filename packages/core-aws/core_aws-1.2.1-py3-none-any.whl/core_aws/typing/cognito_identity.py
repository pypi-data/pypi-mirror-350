# -*- coding: utf-8 -*-


class CognitoIdentity:
    """ Information related to the AWS Cognito identity that authorize the request """

    def __init__(self, cognito_identity_id: str, cognito_identity_pool_id: str) -> None:
        """
        :param cognito_identity_id: The authenticated Amazon Cognito identity.
        :param cognito_identity_pool_id: The Amazon Cognito identity pool that authorized the invocation.
        """

        self._cognito_identity_id = cognito_identity_id
        self._cognito_identity_pool_id = cognito_identity_pool_id

    @property
    def cognito_identity_id(self) -> str:
        return self._cognito_identity_id

    @property
    def cognito_identity_pool_id(self) -> str:
        return self._cognito_identity_pool_id
