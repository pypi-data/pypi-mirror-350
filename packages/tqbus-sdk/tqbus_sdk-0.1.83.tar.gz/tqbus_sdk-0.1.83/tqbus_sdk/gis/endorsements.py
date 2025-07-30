import dataclasses
from typing import List, Optional

from tqbus_sdk.tqsystem import TqSystem, TqSystemConfig, TqSystemEnums


@dataclasses.dataclass
class EndorsementService:
    """
    A class representing an general insurance endorsement service.

    Attributes:
        config (Optional[TqSystemConfig]): Configuration for the TqSystem.
        system (TqSystem): The TqSystem object representing the system.
    """

    config: Optional[TqSystemConfig] = None
    system: TqSystem = dataclasses.field(init=False)

    def __post_init__(self):
        self.system = TqSystem(tq_system_enum=TqSystemEnums.GIS, config=self.config)

    def renew_policy_as_is(self, policy_no: str) -> dict:
        """
        Renews a general insurance policy as is.

        Args:
            policy_no (str): The general insurance policy number.

        Returns:
            dict: The response data.
        """
        url = self.system.base_url + "endorsements/v1/policy-renewal"
        payload = {"policyNo": policy_no}
        data = self.system.request("post", url, json=payload)
        return data

    def enquire_renewal(self, policy_no: str) -> List[dict]:
        """
        Enquires about a general insurance policy renewal.

        Args:
            policy_no (str): The a general insurance policy number.

        Returns:
            List[dict]: The response data.
        """
        url = self.system.base_url + "apis/v2/policies/renewalEnquiry"
        params = {"policyNo": policy_no}
        data = self.system.request("get", url, params=params)
        return data
