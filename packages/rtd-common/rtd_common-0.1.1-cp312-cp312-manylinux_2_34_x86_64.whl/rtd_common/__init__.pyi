from enum import Enum

class RTDType(Enum):
    PT100 = 0
    PT500 = 1
    PT1000 = 2
    Cu10 = 3
    Cu50 = 4
    Cu100 = 4
    Ni100 = 6
    Ni120 = 7
    Ni1000 = 8

class TCType(Enum):
    E = 0
    J = 1
    K = 2
    N = 3
    R = 4
    S = 5
    T = 6
    B = 7

class ChannelType(Enum):
    @classmethod
    def RTD(rtd_type: RTDType): ...

    @classmethod
    def TC(tc_type: TCType): ...

class ChannelConfig:
    def __init__(
            self,
            channel_type: ChannelType,
            max_resistance: float,
            min_resistance: float,
            shunt_resistance: float,
            r_ain0: float
        ): ...


def set_channel_request(channel_number: int, channel_config: ChannelConfig, id: int) -> bytes: ...

def set_temperature_request(channel_number: int, temperature: float, id: int) -> bytes: ...
