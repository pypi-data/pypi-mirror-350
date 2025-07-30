"""DLMS UA 1000-2 Ed. 10"""
from dataclasses import dataclass
from typing import Never
from ..base import CommunicationProfile, Parameters


@dataclass
class MBUSParameters(Parameters):
    """10.5.3 Use of the communication layers for this profile"""

    def validate(self) -> Never:
        """RuntimeError :raise if not valid"""
        raise RuntimeError("not support now")


@dataclass
class MBUS(CommunicationProfile):
    """10.5 The wired and wireless M-Bus profile"""
    parameters: MBUSParameters
