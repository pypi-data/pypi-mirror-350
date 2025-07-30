# -*- coding: utf-8 -*-


class MobileClient:
    """ Mobile Client context that is provided by the client application """

    def __init__(
            self, installation_id: str, app_title: str, app_version_name: str,
            app_version_code: str, app_package_name: str) -> None:

        """
        :param installation_id:
        :param app_title:
        :param app_version_name:
        :param app_version_code:
        :param app_package_name:
        """

        self._installation_id = installation_id
        self._app_title = app_title
        self._app_version_name = app_version_name
        self._app_version_code = app_version_code
        self._app_package_name = app_package_name

    @property
    def installation_id(self) -> str:
        return self._installation_id

    @property
    def app_title(self) -> str:
        return self._app_title

    @property
    def app_version_name(self) -> str:
        return self._app_version_name

    @property
    def app_version_code(self) -> str:
        return self._app_version_code

    @property
    def app_package_name(self) -> str:
        return self._app_package_name
