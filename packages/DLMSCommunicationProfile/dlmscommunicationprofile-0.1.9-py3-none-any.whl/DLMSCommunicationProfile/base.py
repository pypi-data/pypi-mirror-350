from abc import ABC
from dataclasses import dataclass


@dataclass
class Parameters(ABC):
    """"""


@dataclass
class CommunicationProfile(ABC):
    """DLMS UA 1000-2 Ed. 10, 10.1 Communication profile specific elements"""
    parameters: Parameters
