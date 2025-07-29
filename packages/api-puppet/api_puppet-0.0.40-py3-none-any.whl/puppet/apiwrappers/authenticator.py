import base64
from abc import ABC, abstractmethod

from .dto import RequestConfig


class Authenticator(ABC):
    @abstractmethod
    def apply_auth_to_request(self, request_config: RequestConfig) -> RequestConfig:
        raise NotImplementedError()

    @abstractmethod
    def initialize(self):
        raise NotImplementedError()

    @abstractmethod
    def renew_auth(self):
        raise NotImplementedError()


class BasicAuth(Authenticator):
    def __init__(self):
        self._username: str = None
        self._password: str = None
        self._base64_credentials: str = None

    def apply_auth_to_request(self, request_config: RequestConfig) -> RequestConfig:
        if not all([self._username, self._password, self._base64_credentials]):
            raise ValueError("")

        request_config.headers["Authorization"] = f"Basic {self._base64_credentials}"
        return request_config

    def initialize(self):
        self._username = self.get_username()
        self._password = self.get_password()

        if not all([self._username, self._password]):
            raise AttributeError("Attributes 'username' or 'password' are incorrectly set.")

        self._base64_credentials = self._parse_credentials(self._username, self._password)

    def renew_auth(self):
        self._username = self.get_username()
        self._password = self.get_password()

        if not all([self._username, self._password]):
            raise AttributeError("Attributes 'username' or 'password' are incorrectly set.")

        self._base64_credentials = self._parse_credentials(self._username, self._password)

    @abstractmethod
    def get_password(self) -> str:
        """
        Returns the password has a string
        :return: The password string
        """
        raise NotImplementedError()

    @abstractmethod
    def get_username(self) -> str:
        """
        Returns the username has a string
        :return: The username string
        """
        raise NotImplementedError()

    @staticmethod
    def _parse_credentials(user, password):
        credentials = f"{user}:{password}"
        return base64.b64encode(credentials.encode('utf-8')).decode('utf-8')


class HttpHeaderAuth(Authenticator):
    def __init__(self):
        self._header_key_name: str = None
        self._api_key: str = None

    def apply_auth_to_request(self, request_config: RequestConfig) -> RequestConfig:
        request_config.headers[self._header_key_name] = self._api_key
        return request_config

    def initialize(self) -> None:
        self._api_key = self.get_api_key()
        self._header_key_name = self.get_header_key_name()

        if not all([self._api_key, self._header_key_name]):
            raise AttributeError("Attributes 'api_key' or 'header_key_name' are incorrectly set.")

    def renew_auth(self) -> None:
        self._api_key = self.get_api_key()
        self._header_key_name = self.get_header_key_name()

    @abstractmethod
    def get_api_key(self) -> str:
        """
        Returns the api key has a string
        :return: The api key string
        """
        raise NotImplementedError()

    @abstractmethod
    def get_header_key_name(self) -> str:
        """
        Returns the header key name has a string
        :return: The header key name string
        """
        raise NotImplementedError()


class UrlTokenAuth(Authenticator, ABC):
    def __init__(self):
        self._token_name: str = None
        self._token: str = None

    def apply_auth_to_request(self, request_config: RequestConfig) -> RequestConfig:
        request_config.query_params[self._token_name] = self._token
        return request_config

    def initialize(self) -> None:
        self._token = self.get_token()
        self._token_name = self.get_token_name()

        if not all([self._token, self._token_name]):
            raise AttributeError("Attributes 'token' or 'token_name' are incorrectly set.")

    def renew_auth(self):
        self._token = self.get_new_token()
        self._token_name = self.get_token_name()

        if not all([self._token, self._token_name]):
            raise AttributeError("Attributes 'token' or 'token_name' are incorrectly set.")

    @abstractmethod
    def get_token(self) -> str:
        """
        Returns the token has a string
        :return: The token string
        """
        raise NotImplementedError()

    @abstractmethod
    def get_token_name(self) -> str:
        """
        Returns the token name has a string
        :return: The token name string
        """
        raise NotImplementedError()

    @abstractmethod
    def get_new_token(self) -> str:
        """
        Returns the token has a string after refreshing it if needed.
        :return: The token string
        """
        raise NotImplementedError()


class BearerTokenAuth(Authenticator, ABC):
    def __init__(self):
        self.token: str = None

    def apply_auth_to_request(self, request_config: RequestConfig) -> RequestConfig:
        request_config.headers["Authorization"] = f"Bearer {self.token}"
        return request_config

    def initialize(self) -> None:
        self.token = self.get_token()

        if not self.token:
            raise AttributeError("Attribute 'token' is incorrectly set.")

    def renew_auth(self):
        self.token = self.get_new_token()

        if not self.token:
            raise AttributeError("Attribute 'token' is incorrectly set.")

    @abstractmethod
    def get_token(self) -> str:
        """
        Returns the token name has a string
        :return: The token name string
        """
        raise NotImplementedError()

    @abstractmethod
    def get_new_token(self) -> str:
        """
        Returns the token has a string after refreshing it if needed.
        :return: The token string
        """
        raise NotImplementedError()


class NoAuth(Authenticator):
    def initialize(self) -> None:
        pass

    def apply_auth_to_request(self, request_config: RequestConfig) -> RequestConfig:
        return request_config

    def renew_auth(self):
        pass
