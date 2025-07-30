from typing import Dict, Optional

from pydantic import BaseModel

from tqbus_sdk.banca import generics as _generics_banca
from tqbus_sdk.crm import countries as _countries_crm
from tqbus_sdk.crm import tqclients as _clients_crm
from tqbus_sdk.crm import generics as _generics_crm
from tqbus_sdk.gis import endorsements as _endorsements_gis
from tqbus_sdk.gis import policies as _policies_gis
from tqbus_sdk.gis import quotations as _quotations_gis
from tqbus_sdk.gis import generics as _generics_gis
from tqbus_sdk.lms import generics as _generics_lms
from tqbus_sdk.tqsystem import TqSystemConfig, TqSystemEnums


class CRM(BaseModel):
    config: Optional[TqSystemConfig] = None
    _countries: Optional[_countries_crm.CountryService] = None
    _clients: Optional[_clients_crm.ClientService] = None
    _generics: Optional[_generics_crm.GenericCrmService] = None

    @property
    def countries(self) -> _countries_crm.CountryService:
        if self._countries is None:
            self._countries = _countries_crm.CountryService(config=self.config)
        return self._countries

    @property
    def clients(self) -> _clients_crm.ClientService:
        if self._clients is None:
            self._clients = _clients_crm.ClientService(config=self.config)
        return self._clients

    @property
    def generics(self) -> _generics_crm.GenericCrmService:
        if self._generics is None:
            self._generics = _generics_crm.GenericCrmService(config=self.config)
        return self._generics


class GIS(BaseModel):
    config: Optional[TqSystemConfig] = None
    _endorsements: Optional[_endorsements_gis.EndorsementService] = None
    _policies: Optional[_policies_gis.PolicyService] = None
    _quotations: Optional[_quotations_gis.QuotationService] = None
    _generics: Optional[_generics_gis.GenericGisService] = None

    @property
    def endorsements(self) -> _endorsements_gis.EndorsementService:
        if self._endorsements is None:
            self._endorsements = _endorsements_gis.EndorsementService(config=self.config)
        return self._endorsements

    @property
    def policies(self) -> _policies_gis.PolicyService:
        if self._policies is None:
            self._policies = _policies_gis.PolicyService(config=self.config)
        return self._policies

    @property
    def quotations(self) -> _quotations_gis.QuotationService:
        if self._quotations is None:
            self._quotations = _quotations_gis.QuotationService(config=self.config)
        return self._quotations

    @property
    def generics(self) -> _generics_gis.GenericGisService:
        if self._generics is None:
            self._generics = _generics_gis.GenericGisService(config=self.config)
        return self._generics


class Banca(BaseModel):
    config: Optional[TqSystemConfig] = None
    _generics: Optional[_generics_banca.GenericBancaService] = None

    @property
    def generics(self) -> _generics_banca.GenericBancaService:
        if self._generics is None:
            self._generics = _generics_banca.GenericBancaService(config=self.config)
        return self._generics


class LMSV1(BaseModel):
    config: Optional[TqSystemConfig] = None
    _generics: Optional[_generics_lms.GenericIndV1Service] = None

    @property
    def generics(self) -> _generics_lms.GenericIndV1Service:
        if self._generics is None:
            self._generics = _generics_lms.GenericIndV1Service(config=self.config)
        return self._generics


class LMSV2(BaseModel):
    config: Optional[TqSystemConfig] = None
    _generics: Optional[_generics_lms.GenericIndV2Service] = None

    @property
    def generics(self) -> _generics_lms.GenericIndV2Service:
        if self._generics is None:
            self._generics = _generics_lms.GenericIndV2Service(config=self.config)
        return self._generics


ClientConfig = Dict[TqSystemEnums, TqSystemConfig]


class Client(BaseModel):
    config: Optional[ClientConfig] = None

    @property
    def crm(self) -> CRM:
        return CRM(config=self.config.get(TqSystemEnums.CRM) if self.config else None)

    @property
    def gis(self) -> GIS:
        return GIS(config=self.config.get(TqSystemEnums.GIS) if self.config else None)

    @property
    def banca(self) -> Banca:
        return Banca(config=self.config.get(TqSystemEnums.BANCA) if self.config else None)

    @property
    def lmsv1(self) -> LMSV1:
        return LMSV1(config=self.config.get(TqSystemEnums.IND_V1) if self.config else None)

    @property
    def lmsv2(self) -> LMSV2:
        return LMSV2(config=self.config.get(TqSystemEnums.IND_V2) if self.config else None)
