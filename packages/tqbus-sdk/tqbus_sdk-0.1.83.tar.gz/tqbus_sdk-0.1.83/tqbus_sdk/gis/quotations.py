import dataclasses
import datetime
import logging
from typing import List, Optional

import requests.exceptions
from pydantic import BaseModel, Field

from tqbus_sdk.tqsystem import TqDefaultConfig, TqSystem, TqSystemConfig, TqSystemEnums

logger = logging.getLogger(__name__)


class QuotRiskSection(BaseModel):
    sectionCode: int = Field(default=3514)
    limitAmount: float
    premiumRate: Optional[float] = Field(default=None)


class QuoteRisk(BaseModel):
    propertyId: str
    itemDesc: str = Field(default="")
    withEffectFromDate: datetime.date = Field(default_factory=datetime.datetime.now().date)
    withEffectToDate: datetime.date = Field(default_factory=lambda: datetime.datetime.now().date() + datetime.timedelta(days=365))
    binderCode: Optional[int] = Field(default=20207249)
    coverTypeCode: Optional[int] = Field(default=302)
    insuredCode: Optional[int] = Field(default=None)
    location: Optional[str] = Field(default="HEADOFFICE")
    town: Optional[str] = Field(default="LAGOS")
    riskPremAmount: Optional[float] = Field(default=None)
    quotationRiskSections: List[QuotRiskSection] = Field(default_factory=list)
    riskAdditionalInfo: Optional[dict] = Field(default_factory=dict)

    class Config:
        json_encoders = {
            datetime.date: TqDefaultConfig.date_encoder,
            datetime.datetime: TqDefaultConfig.datetime_encoder,
        }
        json_decoders = {
            datetime.date: TqDefaultConfig.date_decoder,
            datetime.datetime: TqDefaultConfig.datetime_decoder,
        }


class QuotationDTO(BaseModel):
    clientCode: Optional[int]
    agentCode: Optional[int] = Field(default=0)
    productCode: Optional[int] = Field(default=7275)
    branchCode: Optional[int] = Field(default=1)
    currencyCode: Optional[int] = Field(default=268)
    coverFromDate: Optional[datetime.date] = Field(default_factory=datetime.datetime.now().date)
    coverToDate: Optional[datetime.date] = Field(default_factory=lambda: datetime.datetime.now().date() + datetime.timedelta(days=365))
    paymentFrequency: Optional[str] = Field(default="A")
    prospectCode: Optional[float] = Field(default=None)
    quotationRisks: List[QuoteRisk] = Field(default_factory=list)
    introducerCode: Optional[float] = Field(default=None)
    paymentMode: Optional[float] = Field(default=None)

    class Config:
        json_encoders = {
            datetime.date: TqDefaultConfig.date_encoder,
            datetime.datetime: TqDefaultConfig.datetime_encoder,
        }
        json_decoders = {
            datetime.date: TqDefaultConfig.date_decoder,
            datetime.datetime: TqDefaultConfig.datetime_decoder,
        }


class QuotationResponse(BaseModel):
    code: Optional[int]
    quotationNumber: Optional[str] = Field(default=None, alias="quotationNumber")
    quotationRevisionNumber: Optional[float] = Field(default=None, alias="quotationRevisionNumber")
    premiumAmount: Optional[float] = Field(default=None, alias="premiumAmount")
    ready: Optional[str] = Field(default=None)


@dataclasses.dataclass
class QuotationService:
    """
    This class represents a general insurance quotation service that provides
    methods for generating
    general insurance quotations and converting them into policies.

    Attributes:
        config (Optional[TqSystemConfig]): Configuration for the TqSystem.
        system (TqSystem): The TqSystem object representing the system
        configuration.
    """

    config: Optional[TqSystemConfig] = None
    system: TqSystem = dataclasses.field(init=False)

    def __post_init__(self):
        self.system = TqSystem(tq_system_enum=TqSystemEnums.GIS, config=self.config)

    def quick_quote(self, client_code: int, property_id: str, limit_amount: float) -> QuotationResponse:
        """
        Generates a quick general insurance quotation based on the provided
        client code, property ID, and limit amount.

        Args:
            client_code (int): The client code.
            property_id (str): The property ID.
            limit_amount (float): The limit amount.

        Returns:
            QuotationResponse: The quotation response object.
        """
        quote_risk_section: QuotRiskSection = QuotRiskSection(limitAmount=limit_amount)
        quote_risk: QuoteRisk = QuoteRisk(
            propertyId=property_id,
            itemDesc=property_id,
            quotationRiskSections=[
                quote_risk_section,
            ],
        )

        quotation_dto: QuotationDTO = QuotationDTO(
            clientCode=client_code,
            quotationRisks=[
                quote_risk,
            ],
        )

        url = self.system.base_url + "quotations/v2/quote-creation"
        payload = quotation_dto.model_dump(mode="json")
        data = self.system.request("post", url, json=payload)
        response = QuotationResponse(**data["payload"])
        logger.debug(f"quote_response={response}")
        return response

    def convert(self, quote_code: int, request_params=None) -> str:
        """
        Converts a general insurance quotation into a general insurance policy
        based on the provided quote code and request parameters.

        Args:
            quote_code (int): The quote code.
            request_params (dict, optional): The request parameters. Defaults to None.

        Returns:
            str: The policy number.
        """
        if request_params is None:
            request_params = {
                "isCoinsurancePolicy": "N",
                "isCoinsuranceLeader": "N",
                "coinsuranceGross": "N",
                "isPolicyRenewable": "Y",
            }
        request_params["quotCode"] = quote_code
        url = self.system.base_url + "quotations/v2/quotation-conversion"
        data = self.system.request("post", url, params=request_params)
        logger.debug(f"quote conversion response={data}")
        try:
            payload = data.get("payload")
            policy_no = payload[0]["policyNumber"]
        except (TypeError, KeyError):
            raise requests.exceptions.HTTPError(data) from None
        logger.debug(f"policy_no={policy_no}")
        return policy_no
