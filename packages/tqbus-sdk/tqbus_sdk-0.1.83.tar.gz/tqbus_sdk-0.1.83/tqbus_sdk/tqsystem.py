import dataclasses
import datetime
import logging
import os
from enum import Enum, auto, unique
from typing import Any, Optional, TypedDict

import requests

logger = logging.getLogger(__name__)


@unique
class TqSystemEnums(Enum):
    CRM = auto()
    GIS = auto()
    IND_V1 = auto()
    IND_V2 = auto()
    BANCA = auto()


class TqDefaultConfig:
    @staticmethod
    def get_var(
        suffix: str,
        tq_sys_enum: Optional[TqSystemEnums] = None,
        raise_error: bool = True,
    ) -> str:
        if tq_sys_enum:
            key = f"TQBUS_{tq_sys_enum.name}_{suffix}"
        else:
            key = f"TQBUS_{suffix}"
        var = os.getenv(key)
        if raise_error and not var:
            raise ValueError(f"{key} env var not set!")
        return var

    @staticmethod
    def date_encoder(dt: Optional[datetime.date]) -> Optional[str]:
        default_date_format = "%Y-%m-%d"
        if not dt:
            return dt
        DATEFORMAT = TqDefaultConfig.get_var("DATEFORMAT", None, False) or default_date_format
        return dt.strftime(DATEFORMAT)

    @staticmethod
    def datetime_encoder(dt: Optional[datetime.datetime]) -> Optional[str]:
        default_datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        if not dt:
            return dt
        DATETIMEFORMAT = TqDefaultConfig.get_var("DATETIMEFORMAT", None, False) or default_datetime_format
        return dt.strftime(DATETIMEFORMAT)

    @staticmethod
    def date_decoder(date_string: Optional[str]) -> Optional[datetime.date]:
        default_date_format = "%Y-%m-%d"
        if not date_string:
            return date_string
        DATEFORMAT = TqDefaultConfig.get_var("DATEFORMAT", None, False) or default_date_format
        return datetime.datetime.strptime(date_string, DATEFORMAT)

    @staticmethod
    def datetime_decoder(date_string: Optional[str]) -> Optional[datetime.datetime]:
        default_datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        if not date_string:
            return date_string
        DATETIMEFORMAT = TqDefaultConfig.get_var("DATETIMEFORMAT", None, False) or default_datetime_format
        return datetime.datetime.strptime(date_string, DATETIMEFORMAT)


@dataclasses.dataclass
class TokenManager:
    auth_url: str
    username: str
    password: str
    __token: str = dataclasses.field(default=None)
    __expires_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.utcnow)

    def generate_token(self, request_kwargs=None) -> None:
        """Generate authentication token using credentials.
        
        Args:
            request_kwargs: Optional kwargs for the requests library (e.g., verify=False)
        """
        if request_kwargs is None:
            request_kwargs = {}
            
        url = self.auth_url
        if not url:
            self.__token = "NO_AUTH_URL"
            self.__expires_at = self.__expires_at + datetime.timedelta(seconds=1000 * 3)
            return
        headers = {"Content-Type": "application/json"}
        payload = {"username": self.username, "password": self.password}
        
        response = requests.post(
            url=url, 
            headers=headers, 
            json=payload,
            **request_kwargs
        )
        response.raise_for_status()
        body = response.json()
        if not body.get("success"):
            raise requests.exceptions.RequestException(body)
        self.__token = body["token"]
        expires_in: int = body["expires_in"]
        # using last generated instead of utcnow() to allow room for error
        self.__expires_at = self.__expires_at + datetime.timedelta(seconds=expires_in / 1000)

    def token(self, request_kwargs=None):
        """Get authentication token, generating a new one if needed.
        
        Args:
            request_kwargs: Optional kwargs for the requests library (e.g., verify=False)
        """
        if not self.__token or datetime.datetime.utcnow() >= self.__expires_at:
            self.generate_token(request_kwargs)
        return self.__token


class TqSystemConfig(TypedDict, total=False):
    """Configuration for TqSystem.
    
    Attributes:
        base_url: Base URL for API requests
        username: Username for authentication
        password: Password for authentication
        request_kwargs: Optional kwargs passed to all requests.request() calls
            Examples: {"verify": False} to disable SSL verification,
                     {"timeout": 30} to set request timeout,
                     {"proxies": {...}} to configure proxies
    """
    base_url: str
    username: str
    password: str
    request_kwargs: dict


@dataclasses.dataclass
class TqSystem:
    """
    Represents a TqSystem object that interacts with a TqSystemEnums instance and a TokenManager instance.

    Attributes:
        tq_system_enum (TqSystemEnums): The TqSystemEnums instance representing the type of TqSystem.
        config (Optional[TqSystemConfig]): Optional configuration dictionary.
        token_manager (Optional[TokenManager]): The TokenManager instance for managing authentication tokens.

    Methods:
        __post_init__(): Initializes the TqSystem object and creates a token manager if not already created.
        _get_env_var(suffix: str) -> str: Retrieves an environment variable based on the given suffix.
        base_url() -> str: Returns the base URL for the TqSystem.
        username() -> Optional[str]: Returns the username for authentication.
        password() -> Optional[str]: Returns the password for authentication.
        auth_url() -> Optional[str]: Returns the authentication URL based on the TqSystemEnums.
        get_default_headers(authenticated: bool) -> dict: Returns the default headers for API requests.
        request(method: str, url: str, **kwargs) -> Any: Sends an HTTP request with the specified method and URL.

    """

    tq_system_enum: TqSystemEnums
    config: Optional[TqSystemConfig] = None
    token_manager: Optional[TokenManager] = dataclasses.field(default=None)

    def __post_init__(self):
        """
        Initializes the TqSystem object and creates a token manager if not already created.
        """
        if not self.token_manager:
            auth_url_val = self.auth_url
            username_val = self.username
            password_val = self.password

            if auth_url_val and username_val and password_val:
                self.token_manager = TokenManager(
                    auth_url=auth_url_val,
                    username=username_val,
                    password=password_val,
                )

    def _get_env_var(self, suffix: str) -> str:
        """
        Retrieves an environment variable based on the given suffix.

        Args:
            suffix (str): The suffix of the environment variable.

        Returns:
            str: The value of the environment variable.

        """
        return TqDefaultConfig.get_var(suffix, self.tq_system_enum)

    @property
    def base_url(self) -> str:
        """
        Returns the base URL for the TqSystem.

        Returns:
            str: The base URL.

        """
        if self.config and isinstance(self.config.get("base_url"), str) and self.config["base_url"]:
            return self.config["base_url"]
        return self._get_env_var("BASEURL")

    @property
    def username(self) -> Optional[str]:
        """
        Returns the username for authentication.

        Returns:
            Optional[str]: The username, or None if not determinable.

        """
        if self.config and isinstance(self.config.get("username"), str):
            # Allow empty string from config if explicitly set, though auth might fail
            return self.config["username"]
        if not self.auth_url:  # If auth_url is None, username cannot be determined for auth
            return None
        return self._get_env_var("USERNAME")  # This might raise if not found and raise_error=True

    @property
    def password(self) -> Optional[str]:
        """
        Returns the password for authentication.

        Returns:
            Optional[str]: The password, or None if not determinable.

        """
        if self.config and isinstance(self.config.get("password"), str):
            # Allow empty string from config
            return self.config["password"]
        if not self.auth_url:  # If auth_url is None, password cannot be determined for auth
            return None
        return self._get_env_var("PASSWORD")  # This might raise if not found and raise_error=True

    @property
    def auth_url(self) -> Optional[str]:
        """
        Returns the authentication URL based on the TqSystemEnums.

        Returns:
            Optional[str]: The authentication URL, or None if not applicable or base_url is missing.

        """
        current_base_url = self.base_url  # This will try config then env, or raise
        # If TqDefaultConfig.get_var is called with raise_error=False and var is not found,
        # current_base_url could be a default value or None. Assuming it raises or returns valid str for now.

        urls_dict: dict[TqSystemEnums, str] = {
            TqSystemEnums.CRM: f"{current_base_url}authenticate/login",
            TqSystemEnums.GIS: f"{current_base_url}oauth/token",
            TqSystemEnums.IND_V2: f"{current_base_url}authenticate/login",
        }
        return urls_dict.get(self.tq_system_enum)  # .get() returns None if key is not found

    def get_default_headers(self, authenticated=True) -> dict:
        """
        Returns the default headers for API requests.

        Args:
            authenticated (bool): Flag indicating whether the request requires authentication.

        Returns:
            dict: The default headers.

        """
        headers = {"Content-Type": "application/json"}
        if not authenticated:
            return headers
        # Get request_kwargs from config if available
        request_kwargs = {}
        if self.config and isinstance(self.config.get("request_kwargs"), dict):
            request_kwargs = self.config["request_kwargs"]
            
        token = self.token_manager.token(request_kwargs)
        headers["Authorization"] = f"Bearer {token}"
        return headers

    def request(self, method: str, url: str, **kwargs) -> Any:
        """
        Sends an HTTP request with the specified method and URL.

        Args:
            method (str): The HTTP method for the request.
            url (str): The URL for the request.
            **kwargs: Additional keyword arguments to be passed to the requests library.
                      These will override any request_kwargs specified in the config.
                      Examples:
                        - verify=False: Disable SSL certificate verification
                        - timeout=30: Set request timeout in seconds
                        - proxies={...}: Configure proxy settings

        Returns:
            Any: The response data.

        Raises:
            requests.exceptions.RequestException: If the request fails.

        """
        # Get default request kwargs from config if available
        default_kwargs = {}
        if self.config and isinstance(self.config.get("request_kwargs"), dict):
            default_kwargs = self.config["request_kwargs"]
        
        # Merge default kwargs with provided kwargs (provided kwargs take precedence)
        request_kwargs = {**default_kwargs, **kwargs}
        
        # Handle headers separately to ensure proper merging
        headers = request_kwargs.get("headers") or self.get_default_headers()
        request_kwargs["headers"] = headers
        
        logger.debug(f"url={url}")
        response = requests.request(method=method, url=url, **request_kwargs)
        logger.debug(f"response: {response}")
        if response.status_code >= 300:  # inject content to reason
            response.reason = response.reason or response.content
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and not data.get("success", True):
            raise requests.exceptions.RequestException(data)
        logger.debug(f"data={data}")
        return data
