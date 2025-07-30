use binrw::{binrw, io::Cursor, BinRead, BinWrite};

use super::{string::String, AsBytes, BaseId, Cmd, Header, Packet};

#[binrw]
#[brw(big)]
#[br(import(len: u32))]
#[derive(Debug)]
pub struct Debug {
    #[br(args(len))]
    pub string: String<u32>,
}

impl BaseId for Debug {
    fn base_id() -> u8 {
        0xFF
    }
}

impl Debug {
    pub fn into(self) -> Packet {
        let bytes = self.as_bytes(());
        Packet {
            cmd: Self::base_id(),
            len: bytes.len() as u32,
            data: bytes.into(),
        }
    }
}

impl TryFrom<Packet> for Debug {
    type Error = binrw::Error;

    fn try_from(packet: Packet) -> Result<Self, Self::Error> {
        let mut cursor = Cursor::new(packet.data.as_slices().0);
        Debug::read_args(&mut cursor, (packet.len,))
    }
}
