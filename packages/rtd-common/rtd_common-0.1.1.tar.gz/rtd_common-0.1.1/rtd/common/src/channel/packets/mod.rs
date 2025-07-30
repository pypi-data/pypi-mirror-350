use binrw::{binrw, BinRead, BinWrite};
use hal_common::packets::{BaseId, Cmd, Header};
use set_channel::{SetChannelRequest, SetChannelResponse};

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

pub mod set_channel;

pub const BASE_ID: u8 = 0x10; // reserves 0x10 to 0x14 as the card has 4 channels

#[binrw]
#[brw(big)]
#[br(import(header: &Header, len: usize))]
#[derive(Debug)]
pub enum Request<
    T: for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>,
> {
    General(#[br(args(header, len))] GeneralRequest),
    Impl(#[br(args(header, len))] T),
}

impl<T: for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>> BaseId
    for Request<T>
{
    fn base_id() -> u8 {
        BASE_ID
    }
}

impl<
        T: Cmd + for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>,
    > Cmd for Request<T>
{
    fn cmd(&self) -> u8 {
        match self {
            Request::General(r) => r.cmd(),
            Request::Impl(t) => t.cmd(),
        }
    }
}

impl Cmd for GeneralRequest {
    fn cmd(&self) -> u8 {
        match self {
            GeneralRequest::SetChannel(_) => 0x00,
            GeneralRequest::SysReset() => 0x01,
        }
    }
}

#[binrw]
#[br(big, import(header: &Header, _len: usize))]
#[derive(Debug)]
pub enum Response<
    T: for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>,
> {
    General(#[br(args(header, _len))] GeneralResponse),
    Impl(#[br(args(header, _len))] T),
}

impl<T: for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>> BaseId
    for Response<T>
{
    fn base_id() -> u8 {
        BASE_ID
    }
}

impl<
        T: Cmd + for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>,
    > Cmd for Response<T>
{
    fn cmd(&self) -> u8 {
        match self {
            Response::General(r) => r.cmd(),
            Response::Impl(t) => t.cmd(),
        }
    }
}

impl Cmd for GeneralResponse {
    fn cmd(&self) -> u8 {
        match self {
            GeneralResponse::SetChannel(_) => 0x00,
        }
    }
}

#[binrw]
#[brw(big)]
#[br(import(header: &Header, _len: usize))]
#[derive(Debug, Clone)]
pub enum GeneralRequest {
    #[br(pre_assert(header.cmd == 0x00))]
    SetChannel(SetChannelRequest),
    #[br(pre_assert(header.cmd == 0x01))]
    SysReset(),
}

#[binrw]
#[br(big, import(header: &Header, _len: usize))]
#[derive(Debug, Clone)]
pub enum GeneralResponse {
    #[br(pre_assert(header.cmd == 0x00))]
    SetChannel(SetChannelResponse),
}

#[cfg(feature = "pyo3")]
pub(crate) fn pymodule(py: Python) -> PyResult<pyo3::Bound<'_, pyo3::types::PyModule>> {
    PyModule::new(py, "packets").map(|module| {
        let submodule = &set_channel::pymodule(py)?;
        py.import("sys")?
            .getattr("modules")?
            .set_item("rtd_common.channel.packets.set_channel", submodule)?;
        module.add_submodule(submodule)?;
        Ok(module)
    })?
}
