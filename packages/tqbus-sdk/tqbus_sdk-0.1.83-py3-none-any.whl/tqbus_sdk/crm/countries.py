import dataclasses
from typing import Any, List, Optional

from pydantic import BaseModel

from tqbus_sdk.tqsystem import TqSystem, TqSystemConfig, TqSystemEnums


class Country(BaseModel):
    code: int
    short_description: Optional[str]
    name: Optional[str]
    nationality: Any
    zip_code: Any
    mobile_prefix: Any
    currency_serial: Any


@dataclasses.dataclass
class CountryService:
    """
    A service class for retrieving country data.
    """

    config: Optional[TqSystemConfig] = None
    system: TqSystem = dataclasses.field(init=False)

    def __post_init__(self):
        self.system = TqSystem(tq_system_enum=TqSystemEnums.CRM, config=self.config)

    def get(self) -> List[Country]:
        """
        Retrieves a list of countries.

        Returns:
            A list of Country objects.
        """
        url = self.system.base_url + "countries"
        data = self.system.request("get", url)
        return [Country(**_) for _ in data]
