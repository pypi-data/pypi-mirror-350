use binrw::binrw;
use hal_common::packets::{Cmd, Header};
use set_temperature::{SetTemperatureRequest, SetTemperatureResponse};

pub mod set_temperature;

#[binrw]
#[brw(big)]
#[br(import(header: &Header, _len: usize))]
#[derive(Debug)]
pub enum Request {
    #[br(pre_assert(header.cmd == 0xF0))]
    SetTemperature(SetTemperatureRequest),
}

impl Cmd for Request {
    fn cmd(&self) -> u8 {
        match self {
            Request::SetTemperature(_) => 0xF0,
        }
    }
}

#[binrw]
#[br(big, import(header: &Header, _len: usize))]
#[derive(Debug)]
pub enum Response {
    #[br(pre_assert(header.cmd == 0xF0))]
    SetTemperature(SetTemperatureResponse),
}

impl Cmd for Response {
    fn cmd(&self) -> u8 {
        match self {
            Response::SetTemperature(_) => 0xF0,
        }
    }
}
