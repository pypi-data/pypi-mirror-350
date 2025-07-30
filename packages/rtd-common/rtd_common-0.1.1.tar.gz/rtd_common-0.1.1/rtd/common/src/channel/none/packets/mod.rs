use binrw::binrw;
use hal_common::packets::{Cmd, Header};
use set_meas_pins::{SetMeasPinsRequest, SetMeasPinsResponse};
use set_meas_resistance::{SetMeasResistanceRequest, SetMeasResistanceResponse};

pub mod set_meas_pins;
pub mod set_meas_resistance;

#[binrw]
#[brw(big)]
#[br(import(header: &Header, _len: usize))]
#[derive(Debug)]
pub enum Request {
    #[br(pre_assert(header.cmd == 0xF0))]
    SetMeasResistance(SetMeasResistanceRequest),
    #[br(pre_assert(header.cmd == 0xF1))]
    SetMeasPins(SetMeasPinsRequest),
}

impl Cmd for Request {
    fn cmd(&self) -> u8 {
        match self {
            Request::SetMeasResistance(_) => 0xF0,
            Request::SetMeasPins(_) => 0xF1,
        }
    }
}

#[binrw]
#[br(big, import(header: &Header, _len: usize))]
#[derive(Debug)]
pub enum Response {
    #[br(pre_assert(header.cmd == 0xF0))]
    SetMeasResistance(SetMeasResistanceResponse),
    #[br(pre_assert(header.cmd == 0xF1))]
    SetMeasPins(SetMeasPinsResponse),
}

impl Cmd for Response {
    fn cmd(&self) -> u8 {
        match self {
            Response::SetMeasResistance(_) => 0xF0,
            &Response::SetMeasPins(_) => 0xF1,
        }
    }
}
