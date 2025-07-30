"""DLMS UA 1000-2 Ed. 10"""
from dataclasses import dataclass, field
from ..base import CommunicationProfile, Parameters
from .. import limit
from .negotiation import Negotiation


window_size_values = limit.MinMax(
    name="window size",
    min=1,
    max=7
)
info_field_length_values = limit.MinMax(
    name="info field length",
    min=32,
    max=2030
)


@dataclass
class HDLCParameters(Parameters):
    """8.4 Protocol specification for the MAC sublayer"""
    comm_speed: int = 9600
    window_size_transmit: int = 1
    window_size_receive: int = 1
    max_info_field_length_transmit: int = 128
    max_info_field_length_receive: int = 128
    inter_octet_time_out: int = 25
    inactivity_time_out: int = 120
    device_address: int | None = 0x10
    """physical address from HDLC setup, lower address in HDLC frame"""

    def validate(self) -> None:
        """RuntimeError :raise if not valid"""
        window_size_values.validate(self.window_size_transmit)
        window_size_values.validate(self.window_size_receive)
        info_field_length_values.validate(self.max_info_field_length_transmit)
        info_field_length_values.validate(self.max_info_field_length_receive)


@dataclass
class HDLC(CommunicationProfile):
    """10.2 The 3-layer, connection-oriented, HDLC based communication profile"""
    parameters: HDLCParameters = field(default_factory=HDLCParameters)
    negotiation: Negotiation = field(init=False)  # todo: temporary need refactoring

    def __post_init__(self) -> None:
        self.negotiation = Negotiation(
            max_info_receive=self.parameters.max_info_field_length_receive,
            max_info_transmit=self.parameters.max_info_field_length_transmit,
            window_receive=self.parameters.window_size_receive,
            window_transmit=self.parameters.window_size_transmit
        )
