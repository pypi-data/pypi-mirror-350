import dataclasses
import datetime
import logging
from typing import Any, List, Optional

import exrex
import requests
from pydantic import BaseModel, Field

from tqbus_sdk.tqsystem import TqDefaultConfig, TqSystem, TqSystemConfig, TqSystemEnums

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class ClientType:
    code: int
    name: Optional[str]
    category: Optional[str]
    description: Optional[str]
    type: str


class ClientQueryParam(BaseModel):
    id_registration_no: Optional[str] = Field(default=None)
    passport_no: Optional[str] = Field(default=None)
    client_code: Optional[int] = Field(default=None)
    client_type: Optional[str] = Field(default=None)
    email_address: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    page: int = Field(default=0)
    size: int = Field(default=1)
    sht_description: Optional[str] = Field(default=None)
    state_code: Optional[int] = Field(default=None)

    class Config:
        json_encoders = {
            datetime.date: TqDefaultConfig.date_encoder,
            datetime.datetime: TqDefaultConfig.datetime_encoder,
        }
        json_decoders = {
            datetime.date: TqDefaultConfig.date_decoder,
            datetime.datetime: TqDefaultConfig.datetime_decoder,
        }


class Client(BaseModel):
    """
    Represents a client in the system.

    Attributes:
        code (Optional[int]): The client's code.
        short_description (Optional[str]): The short description of the client.
        name (Optional[str]): The client's name.
        other_names (Optional[str]): Other names of the client.
        surname (Optional[str]): The client's surname.
        id_reg_no (Any): The client's identification or registration number.
        date_of_birth (Optional[datetime.date]): The client's date of birth.
        PIN (Optional[str]): The client's PIN.
        town_code (Optional[int]): The code of the town where the client resides.
        country_code (Optional[int]): The code of the country where the client resides.
        zip_code (Optional[int]): The client's zip code.
        date_created (Optional[datetime.datetime]): The date when the client was created.
        direct_client (Optional[str]): Indicates if the client is a direct client.
        state_code (Optional[int]): The code of the state where the client resides.
        branch_code (Optional[int]): The code of the branch where the client belongs.
        payroll_No (Optional[str]): The client's payroll number.
        email_address (Optional[str]): The client's email address.
        telephone (Optional[str]): The client's telephone number.
        status (Optional[str]): The client's status.
        proposer (Optional[str]): Indicates if the client is a proposer.
        account_no (Optional[str]): The client's account number.
        with_effect_from (Optional[datetime.date]): The date when the client's changes take effect from.
        with_effect_to (Optional[datetime.datetime]): The date when the client's changes take effect to.
        type (str): The type of the client.
        gender (Optional[str]): The client's gender.
    """

    code: Optional[int] = Field(default=None)
    short_description: Optional[str] = Field(default_factory=lambda: exrex.getone("^[A-Z0-9]{5}$"))
    name: Optional[str] = Field(default=None)
    other_names: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    id_reg_no: Any = Field(default=None)
    date_of_birth: Optional[datetime.date] = Field(default=None, strict=False)
    PIN: Optional[str] = Field(default=None)
    town_code: Optional[int] = Field(default=544)
    country_code: Optional[int] = Field(default=165)
    zip_code: Optional[int] = Field(default=234)
    date_created: Optional[datetime.datetime] = Field(default=None, strict=False)
    direct_client: Optional[str] = Field(default="N")
    state_code: Optional[int] = Field(default=24)
    branch_code: Optional[int] = Field(default=1)
    payroll_No: Optional[str] = Field(default=None)
    email_address: Optional[str] = Field(default=None)
    telephone: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default="A")
    proposer: Optional[str] = Field(default="Y")
    account_no: Optional[str] = Field(default=None)
    with_effect_from: Optional[datetime.date] = Field(default=None, strict=False)
    with_effect_to: Optional[datetime.datetime] = Field(default=None, strict=False)
    type: str = Field(default="13I")
    gender: Optional[str] = Field(default="B")

    class Config:
        json_encoders = {
            datetime.date: TqDefaultConfig.date_encoder,
            datetime.datetime: TqDefaultConfig.datetime_encoder,
        }
        json_decoders = {
            datetime.date: TqDefaultConfig.date_decoder,
            datetime.datetime: TqDefaultConfig.datetime_decoder,
        }


@dataclasses.dataclass
class ClientService:
    config: Optional[TqSystemConfig] = None
    system: TqSystem = dataclasses.field(init=False)

    def __post_init__(self):
        self.system = TqSystem(tq_system_enum=TqSystemEnums.CRM, config=self.config)

    def get(self, query: ClientQueryParam) -> List[Client]:
        url = self.system.base_url + "clients/query"
        params = query.model_dump(
            exclude_none=True,
        )
        data = self.system.request("get", url, params=params)
        return [Client(**_) for _ in data]

    def create(self, client: Client) -> Client:
        url = self.system.base_url + "v3-create-client"
        payload = {"client": client.model_dump(mode="json")}
        try:
            data = self.system.request("post", url=url, json=payload)
        except (
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException,
        ) as e:
            logger.debug("client creation failsafe, query if created")
            query: ClientQueryParam = ClientQueryParam(id_registration_no=client.id_reg_no, email_address=client.email_address)
            clients = self.get(query=query)
            logger.debug(f"client creation failsafe, results={clients}")
            if clients:
                data = clients[0]
                return data
            else:
                raise e
        return Client(**data)

    def get_client_types(self) -> List[ClientType]:
        url = self.system.base_url + "client-types"
        data = self.system.request("get", url)
        return [ClientType(**_) for _ in data]
