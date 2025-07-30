import dataclasses
from typing import Any, Optional

from tqbus_sdk.tqsystem import TqSystem, TqSystemConfig, TqSystemEnums


@dataclasses.dataclass
class GenericIndV1Service:
    """
    A generic service class for individual life V1 system.

    This class provides methods to make HTTP requests to the individual life V1 system.

    Attributes:
        config (Optional[TqSystemConfig]): Configuration for the TqSystem.
        system (TqSystem): The TqSystem instance representing the individual life V1 system.

    Methods:
        request: Makes an HTTP request to the individual life V1 system.

    """

    config: Optional[TqSystemConfig] = None
    system: TqSystem = dataclasses.field(init=False)

    def __post_init__(self):
        self.system = TqSystem(tq_system_enum=TqSystemEnums.IND_V1, config=self.config)

    def request(self, method: str, url: str, **kwargs) -> Any:
        """
        Makes an HTTP request to the individual life V1 system.

        Args:
            method (str): The HTTP method to use for the request.
            url (str): The URL to send the request to.
            **kwargs: Additional keyword arguments to be passed to the underlying request method.

        Returns:
            Any: The response from the individual life V1 system.

        """
        url = self.system.base_url + url
        return self.system.request(method=method, url=url, **kwargs)


@dataclasses.dataclass
class GenericIndV2Service:
    """
    A generic service class for individual life V2 system.

    This class provides methods to make HTTP requests to the individual life V2 system.

    Attributes:
        config (Optional[TqSystemConfig]): Configuration for the TqSystem.
        system (TqSystem): The TqSystem instance representing the individual life V2 system.

    Methods:
        request: Makes an HTTP request to the individual life V2 system.
    """

    config: Optional[TqSystemConfig] = None
    system: TqSystem = dataclasses.field(init=False)

    def __post_init__(self):
        self.system = TqSystem(tq_system_enum=TqSystemEnums.IND_V2, config=self.config)

    def request(self, method: str, url: str, **kwargs) -> Any:
        """
        Makes an HTTP request to the individual life V2 system.

        Args:
            method (str): The HTTP method to use for the request.
            url (str): The URL to send the request to.
            **kwargs: Additional keyword arguments to be passed to the underlying request method.

        Returns:
            Any: The response from the individual life V2 system.
        """
        url = self.system.base_url + url
        return self.system.request(method=method, url=url, **kwargs)
