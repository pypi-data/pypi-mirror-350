from typing import List, Optional

from deepteam.vulnerabilities import BaseVulnerability
from deepteam.vulnerabilities.custom.custom_types import CustomVulnerabilityType


class CustomVulnerability(BaseVulnerability):
    """
    Custom vulnerability class that allows users to define their own vulnerability types.
    """

    def __init__(
        self,
        name: str,
        types: Optional[List[str]] = None,
        custom_prompt: Optional[str] = None,
    ):
        self.name = name
        self.raw_types = types or []
        self.custom_prompt = custom_prompt

        # Create enum types for each raw type
        enum_types = [
            CustomVulnerabilityType.CUSTOM_VULNERABILITY for _ in self.raw_types
        ]
        super().__init__(types=enum_types)

    def get_name(self) -> str:
        return self.name

    def get_custom_prompt(self) -> Optional[str]:
        return self.custom_prompt

    def get_raw_types(self) -> List[str]:
        """Get the original string type values"""
        return self.raw_types
