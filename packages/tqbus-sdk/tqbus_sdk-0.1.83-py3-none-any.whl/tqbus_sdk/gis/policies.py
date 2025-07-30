import dataclasses
from typing import List, Optional

from tqbus_sdk.tqsystem import TqSystem, TqSystemConfig, TqSystemEnums


@dataclasses.dataclass
class PolicyService:
    """
    A class representing a general insurance policy service.

    Attributes:
        config (Optional[TqSystemConfig]): Configuration for the TqSystem.
        system (TqSystem): The TqSystem object representing the system.

    Methods:
        query(policy_no: str) -> List[dict]: Retrieves a general insurance policy details for a given a general insurance policy number.
        find(policy_no: str) -> dict: Finds a general insurance policy by its policy number.
    """

    config: Optional[TqSystemConfig] = None
    system: TqSystem = dataclasses.field(init=False)

    def __post_init__(self):
        self.system = TqSystem(tq_system_enum=TqSystemEnums.GIS, config=self.config)

    def query(self, policy_no: str) -> List[dict]:
        """
        Retrieves a general insurance policy details for a given a general insurance policy number.

        Args:
            policy_no (str): The general insurance policy number.

        Returns:
            List[dict]: A list of a general insurance policy details as dictionaries.
        """
        url = self.system.base_url + "apis/v2/policies/policydetails"
        params = {"policyNumber": policy_no}
        data = self.system.request("get", url, params=params)
        return data

    def find(self, policy_no: str) -> dict:
        """
        Finds a general insurance policy by its policy number.

        Args:
            policy_no (str): The general insurance policy number.

        Returns:
            dict: The general insurance policy details as a dictionary.
        """
        data = self.query(policy_no=policy_no)
        item = data[0] if data else data
        return item
