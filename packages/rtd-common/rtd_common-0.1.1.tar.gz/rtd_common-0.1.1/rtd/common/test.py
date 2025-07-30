from hal_common.packets import Request as HalRequest
from rtd_common.channel.packets import Request as RTDRequest, GeneralRequest
from rtd_common.channel.packets.set_channels import (
    SetChannelRequest,
    ChannelConfig,
    ChannelType,
    RTDType
)


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

    set_channel_request = SetChannelRequest(channel_config)
    general_request = GeneralRequest.SetChannel(set_channel_request)
    rtd_request = RTDRequest.General(general_request)

    u8_c_number = chan_number & 0xFF

    msg = HalRequest.with_id(rtd_request, 1).into(u8_c_number).as_bytes()
    return msg
    # base_id: int = Request.General(general_request).base_id()
    # adress: int = chan_number
    # cmd: int = Request.General(general_request).cmd()
