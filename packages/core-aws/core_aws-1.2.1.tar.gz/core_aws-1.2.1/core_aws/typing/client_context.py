# -*- coding: utf-8 -*-

from typing import Dict

from .mobile_client import MobileClient


class ClientContext:
    """ Client context that's provided to Lambda by the client application """

    def __init__(self, client: MobileClient, custom: Dict, env: Dict) -> None:
        """
        :param client: Client context that's provided to Lambda by the client application.
        :param custom: Custom values set by the mobile client application...
        :param env: Environment information provided by the AWS SDK...
        """

        self._client = client
        self._custom = custom
        self._env = env

    @property
    def client(self) -> MobileClient:
        return self._client

    @property
    def custom(self) -> Dict:
        return self._custom

    @property
    def env(self) -> Dict:
        return self._env
