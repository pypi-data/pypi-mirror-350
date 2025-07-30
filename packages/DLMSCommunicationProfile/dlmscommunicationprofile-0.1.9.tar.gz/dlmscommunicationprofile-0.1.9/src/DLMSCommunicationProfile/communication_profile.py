from typing import TypeAlias
from .HDLC.hdlc import HDLC, HDLCParameters
from .TCPUDPIP.tcp_udp_ip import TCPUDPIP, TCPUDPParameters
from .MBUS.m_bus import MBUS, MBUSParameters


CommunicationProfile: TypeAlias = HDLC | TCPUDPIP | MBUS
Parameters: TypeAlias = HDLCParameters | TCPUDPParameters | MBUSParameters
