#[cfg(not(feature = "std"))]
use alloc::{collections::vec_deque::VecDeque, vec::Vec};
#[cfg(feature = "std")]
use std::{collections::vec_deque::VecDeque, vec::Vec};

use binrw::{binrw, io::Cursor, meta::WriteEndian, BinRead, BinWrite};

pub mod debug;
pub mod result;
pub mod string;

pub trait RawPacketHandler {
    fn handle(&mut self, packet: Packet);
}
pub struct NullHandler;
impl RawPacketHandler for NullHandler {
    fn handle(&mut self, _packet: Packet) {}
}

#[derive(Debug, Clone)]
pub struct Packet {
    pub cmd: u8,
    pub len: u32,
    pub data: VecDeque<u8>,
}
impl Packet {
    pub fn from_data(cmd: u8, data: Vec<u8>) -> Self {
        Self {
            cmd,
            len: data.len() as u32,
            data: data.into(),
        }
    }

    pub fn as_bytes(&self) -> Vec<u8> {
        let mut data = Vec::with_capacity(5 + self.data.len());
        data.push(self.cmd);
        data.extend_from_slice(&self.len.to_be_bytes());
        data.extend(self.data.iter());
        data
    }
}

pub trait AsBytes<A> {
    fn as_bytes(&self, args: A) -> Vec<u8>;
}

impl<A, T: for<'a> BinWrite<Args<'a> = A> + WriteEndian> AsBytes<A> for T {
    fn as_bytes(&self, args: A) -> Vec<u8> {
        let mut buf = Cursor::new(Vec::new());
        self.write_args(&mut buf, args).unwrap();
        buf.into_inner()
    }
}

pub trait PacketHandler {
    type Request: for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>;
    type Response: for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>;

    fn handle(&mut self, header: &Header, packet: Self::Request) -> Option<Self::Response>;
}

pub trait BaseId {
    fn base_id() -> u8;
}

pub trait Cmd {
    fn cmd(&self) -> u8;
}

#[binrw]
#[brw(big)]
#[derive(Debug, Clone)]
pub struct Header {
    pub cmd: u8,
    pub id: u32,
}
const HEADER_SIZE: usize = size_of::<u8>() + size_of::<u32>();

#[binrw]
#[brw(big)]
#[br(import(len: usize))]
#[derive(Debug, Clone)]
pub struct Request<
    T: for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>,
> {
    pub header: Header,
    #[br(args(&header, len - HEADER_SIZE))]
    pub request: T,
}

impl<T: for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>>
    TryFrom<Packet> for Request<T>
{
    type Error = binrw::Error;

    fn try_from(packet: Packet) -> Result<Self, Self::Error> {
        let mut cursor = Cursor::new(packet.data.as_slices().0);
        Request::read_args(&mut cursor, (packet.len as usize,))
    }
}

impl<
        T: Cmd + for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>,
    > Request<T>
{
    pub fn with_id(request: T, id: u32) -> Self {
        Self {
            header: Header {
                cmd: request.cmd(),
                id,
            },
            request,
        }
    }
}

impl<
        T: BaseId + for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>,
    > Request<T>
{
    pub fn into(self, address: u8) -> Packet {
        let bytes = self.as_bytes(());
        Packet {
            cmd: T::base_id() + address,
            len: bytes.len() as u32,
            data: bytes.into(),
        }
    }
}

#[binrw]
#[brw(big)]
#[br(import(len: usize))]
#[derive(Debug)]
pub struct Response<
    T: for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>,
> {
    pub header: Header,
    #[br(args(&header, len - HEADER_SIZE))]
    pub response: T,
}

impl<T: for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>>
    TryFrom<Packet> for Response<T>
{
    type Error = binrw::Error;

    fn try_from(packet: Packet) -> Result<Self, Self::Error> {
        let mut cursor = Cursor::new(packet.data.as_slices().0);
        Response::read_args(&mut cursor, (packet.len as usize,))
    }
}

impl<
        T: Cmd + for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>,
    > Response<T>
{
    pub fn with_id(response: T, id: u32) -> Self {
        Self {
            header: Header {
                cmd: response.cmd(),
                id,
            },
            response,
        }
    }
}

impl<
        T: BaseId + for<'a> BinRead<Args<'a> = (&'a Header, usize)> + for<'a> BinWrite<Args<'a> = ()>,
    > Response<T>
{
    pub fn into(self, address: u8) -> Packet {
        let bytes = self.as_bytes(());
        Packet {
            cmd: T::base_id() + address,
            len: bytes.len() as u32,
            data: bytes.into(),
        }
    }
}

// #[cfg(feature = "pyo3")]
// use pyo3::prelude::*;



// #[cfg(feature = "pyo3")]
// pub(crate) fn pymodule(py: Python) -> PyResult<pyo3::Bound<'_, pyo3::types::PyModule>> {
//     PyModule::new(py, "packets").map(|module| {
//         module.add_class::<Request>()?;
//         Ok(module)
//     })?
// }
