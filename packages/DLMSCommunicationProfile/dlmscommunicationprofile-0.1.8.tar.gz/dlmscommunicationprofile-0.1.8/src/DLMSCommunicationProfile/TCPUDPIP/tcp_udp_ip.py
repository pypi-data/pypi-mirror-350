"""DLMS UA 1000-2 Ed. 10"""
from dataclasses import dataclass
from typing import Never
from ..base import CommunicationProfile, Parameters


@dataclass
class TCPUDPParameters(Parameters):
    """7.3.3 Protocol specification for the DLMS/COSEM UDP-based transport layer or 7.4.3"""

    def validate(self) -> Never:
        """RuntimeError :raise if not valid"""
        raise RuntimeError("not support now")


@dataclass
class TCPUDPIP(CommunicationProfile):
    """10.3 The TCP-UDP/IP based communication profiles (COSEM_on_IP)"""
    parameters: TCPUDPParameters
