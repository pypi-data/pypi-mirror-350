import serial

from rtd_common.channel.packets.set_channel import RTDType, ChannelType, ChannelConfig
from rtd_common import set_channel_request, set_temperature_request


def r_ain_0(channel: int):
    match channel:
        case 3:
            return 15.0
        case _:
            return 1.5e3


def set_channel(chan_number: int):
    channel_type = ChannelType.RTD(RTDType.PT100)
    channel_config = ChannelConfig(
        channel_type,
        390.0,
        0.0,
        12.0 + 0.033,
        r_ain_0(chan_number)
    )

    cmd = set_channel_request(chan_number, channel_config, 1)
    return cmd

def set_temperature(chan_number: int):
    j = 53000
    temperature = -225 + j / 65535 * 1700
    cmd = set_temperature_request(chan_number, temperature, j)
    return cmd

print(type(set_temperature(3)))

# with serial.Serial("/dev/ttyACM0",timeout=0.1) as rtd_board:
#     cmd = set_temperature(3)
#     print(cmd)
#     rtd_board.write(cmd)
#     response = rtd_board.readall()
#     print(response)