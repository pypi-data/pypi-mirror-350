#[cfg(not(feature = "std"))]
use alloc::boxed::Box;

#[cfg(not(feature = "std"))]
use alloc::format;

#[cfg(feature = "std")]
use std::boxed::Box;

#[cfg(feature = "std")]
use std::format;

use binrw::{binrw, BinRead, BinWrite};

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum Input {
    AIN0,
    AIN1,
    AIN2,
    AIN3,
    AVSS,
}

pub const VREF: f32 = 2.048;
#[derive(Debug, Copy, Clone, PartialEq)]
pub enum Mux {
    Inputs(Input, Input),
    Reference, // (V(REFP) - V(REFN)) / 4 (PGA bypass)
    Ananlog,   // (AVDD - AVSS) / 4 (PGA bypass)
    Shorted,   // AINP and AINN shorted to (AVDD + AVSS) / 2
    Reserved,
}

impl TryInto<u8> for Mux {
    type Error = ();

    fn try_into(self) -> Result<u8, Self::Error> {
        match self {
            Mux::Inputs(Input::AIN0, Input::AIN1) => Ok(0b0000),
            Mux::Inputs(Input::AIN0, Input::AIN2) => Ok(0b0001),
            Mux::Inputs(Input::AIN0, Input::AIN3) => Ok(0b0010),
            Mux::Inputs(Input::AIN1, Input::AIN0) => Ok(0b0011),
            Mux::Inputs(Input::AIN1, Input::AIN2) => Ok(0b0100),
            Mux::Inputs(Input::AIN1, Input::AIN3) => Ok(0b0101),
            Mux::Inputs(Input::AIN2, Input::AIN3) => Ok(0b0110),
            Mux::Inputs(Input::AIN3, Input::AIN2) => Ok(0b0111),
            Mux::Inputs(Input::AIN0, Input::AVSS) => Ok(0b1000),
            Mux::Inputs(Input::AIN1, Input::AVSS) => Ok(0b1001),
            Mux::Inputs(Input::AIN2, Input::AVSS) => Ok(0b1010),
            Mux::Inputs(Input::AIN3, Input::AVSS) => Ok(0b1011),
            Mux::Reference => Ok(0b1100),
            Mux::Ananlog => Ok(0b1101),
            Mux::Shorted => Ok(0b1110),
            Mux::Reserved => Ok(0b1111),
            _ => Err(()),
        }
    }
}

impl TryFrom<u8> for Mux {
    type Error = ();

    fn try_from(value: u8) -> Result<Self, Self::Error> {
        match value {
            0b0000 => Ok(Mux::Inputs(Input::AIN0, Input::AIN1)),
            0b0001 => Ok(Mux::Inputs(Input::AIN0, Input::AIN2)),
            0b0010 => Ok(Mux::Inputs(Input::AIN0, Input::AIN3)),
            0b0011 => Ok(Mux::Inputs(Input::AIN1, Input::AIN0)),
            0b0100 => Ok(Mux::Inputs(Input::AIN1, Input::AIN2)),
            0b0101 => Ok(Mux::Inputs(Input::AIN1, Input::AIN3)),
            0b0110 => Ok(Mux::Inputs(Input::AIN2, Input::AIN3)),
            0b0111 => Ok(Mux::Inputs(Input::AIN3, Input::AIN2)),
            0b1000 => Ok(Mux::Inputs(Input::AIN0, Input::AVSS)),
            0b1001 => Ok(Mux::Inputs(Input::AIN1, Input::AVSS)),
            0b1010 => Ok(Mux::Inputs(Input::AIN2, Input::AVSS)),
            0b1011 => Ok(Mux::Inputs(Input::AIN3, Input::AVSS)),
            0b1100 => Ok(Mux::Reference),
            0b1101 => Ok(Mux::Ananlog),
            0b1110 => Ok(Mux::Shorted),
            0b1111 => Ok(Mux::Reserved),
            _ => Err(()),
        }
    }
}

impl Mux {
    pub fn try_reverse(&self) -> Result<Mux, ()> {
        match self {
            Mux::Inputs(i1, i2) => {
                let code: Result<u8, _> = Mux::Inputs(*i2, *i1).try_into();
                if code.is_ok() {
                    Ok(Mux::Inputs(*i2, *i1))
                } else {
                    Err(())
                }
            }
            _ => Err(()),
        }
    }
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum Gain {
    G1 = 0b000,
    G2 = 0b001,
    G4 = 0b010,
    G8 = 0b011,
    G16 = 0b100,
    G32 = 0b101,
    G64 = 0b110,
    G128 = 0b111,
}
impl TryFrom<u8> for Gain {
    type Error = ();

    fn try_from(value: u8) -> Result<Self, Self::Error> {
        match value {
            0b000 => Ok(Gain::G1),
            0b001 => Ok(Gain::G2),
            0b010 => Ok(Gain::G4),
            0b011 => Ok(Gain::G8),
            0b100 => Ok(Gain::G16),
            0b101 => Ok(Gain::G32),
            0b110 => Ok(Gain::G64),
            0b111 => Ok(Gain::G128),
            _ => Err(()),
        }
    }
}
impl Gain {
    pub fn as_value(&self) -> u8 {
        match self {
            Gain::G1 => 1,
            Gain::G2 => 2,
            Gain::G4 => 4,
            Gain::G8 => 8,
            Gain::G16 => 16,
            Gain::G32 => 32,
            Gain::G64 => 64,
            Gain::G128 => 128,
        }
    }
}
impl BinWrite for Gain {
    type Args<'a> = ();

    fn write_options<W: binrw::io::Write + binrw::io::Seek>(
        &self,
        writer: &mut W,
        endian: binrw::Endian,
        args: Self::Args<'_>,
    ) -> binrw::BinResult<()> {
        (*self as u8).write_options(writer, endian, args)
    }
}
impl BinRead for Gain {
    type Args<'a> = ();

    fn read_options<R: binrw::io::Read + binrw::io::Seek>(
        reader: &mut R,
        endian: binrw::Endian,
        (): Self::Args<'_>,
    ) -> binrw::BinResult<Self> {
        let value = u8::read_options(reader, endian, ())?;
        Gain::try_from(value).map_err(|_| binrw::Error::BadMagic {
            pos: 0,
            found: Box::new(format!("Invalid Gain value [{:?}]", value)),
        })
    }
}

#[derive(Debug, Copy, Clone)]
pub enum DataRate {
    SPS20 = 0b000,
    SPS45 = 0b001,
    SPS90 = 0b010,
    SPS175 = 0b011,
    SPS330 = 0b100,
    SPS600 = 0b101,
    SPS1000 = 0b110,
    Reserved = 0b111,
}
impl TryFrom<u8> for DataRate {
    type Error = ();

    fn try_from(value: u8) -> Result<Self, Self::Error> {
        match value {
            0b000 => Ok(DataRate::SPS20),
            0b001 => Ok(DataRate::SPS45),
            0b010 => Ok(DataRate::SPS90),
            0b011 => Ok(DataRate::SPS175),
            0b100 => Ok(DataRate::SPS330),
            0b101 => Ok(DataRate::SPS600),
            0b110 => Ok(DataRate::SPS1000),
            0b111 => Ok(DataRate::Reserved),
            _ => Err(()),
        }
    }
}
impl DataRate {
    pub fn as_value(&self) -> u32 {
        match self {
            DataRate::SPS20 => 20,
            DataRate::SPS45 => 45,
            DataRate::SPS90 => 90,
            DataRate::SPS175 => 175,
            DataRate::SPS330 => 330,
            DataRate::SPS600 => 600,
            DataRate::SPS1000 => 1000,
            DataRate::Reserved => 0,
        }
    }
}

#[derive(Debug, Copy, Clone)]
pub enum OperatingMode {
    Normal = 0, // 256 kHz
    Turbo = 1,  // 512 kHz
}

impl From<bool> for OperatingMode {
    fn from(value: bool) -> Self {
        match value {
            false => OperatingMode::Normal,
            true => OperatingMode::Turbo,
        }
    }
}

#[derive(Debug, Copy, Clone)]
pub enum ConversionMode {
    SingleShot = 0,
    Continuous = 1,
}

impl From<bool> for ConversionMode {
    fn from(value: bool) -> Self {
        match value {
            false => ConversionMode::SingleShot,
            true => ConversionMode::Continuous,
        }
    }
}

#[derive(Debug, Copy, Clone)]
pub enum VoltageReference {
    Internal = 0b00, // 2.048V
    External = 0b01, // REFN and REFP pins
    Analog = 0b10,   // AVDD and AVSS pins
}

impl TryFrom<u8> for VoltageReference {
    type Error = ();

    fn try_from(value: u8) -> Result<Self, Self::Error> {
        match value {
            0b00 => Ok(VoltageReference::Internal),
            0b01 => Ok(VoltageReference::External),
            0b10 | 0b11 => Ok(VoltageReference::Analog),
            _ => Err(()),
        }
    }
}

#[derive(Debug, Copy, Clone)]
pub enum DataIntegrity {
    Disabled = 0b00,
    InvertedOutput = 0b01,
    CRC16 = 0b10,
    Reserved = 0b11,
}

impl TryFrom<u8> for DataIntegrity {
    type Error = ();

    fn try_from(value: u8) -> Result<Self, Self::Error> {
        match value {
            0b00 => Ok(DataIntegrity::Disabled),
            0b01 => Ok(DataIntegrity::InvertedOutput),
            0b10 => Ok(DataIntegrity::CRC16),
            0b11 => Ok(DataIntegrity::Reserved),
            _ => Err(()),
        }
    }
}

pub fn twos_compliment<const SIZE: u8>(value: u32) -> i32 {
    let mask = u32::MAX >> (32u8 - SIZE);
    if value & (1 << (SIZE - 1)) != 0 {
        -(((value - 1) ^ mask & mask) as i32)
    } else {
        (value & mask) as i32
    }
}

#[derive(Debug, Copy, Clone)]
pub enum CurrentSource {
    Off = 0b000,
    C10uA = 0b001,
    C50uA = 0b010,
    C100uA = 0b011,
    C250uA = 0b100,
    C500uA = 0b101,
    C1000uA = 0b110,
    C1500uA = 0b111,
}

impl TryFrom<u8> for CurrentSource {
    type Error = ();

    fn try_from(value: u8) -> Result<Self, Self::Error> {
        match value {
            0b000 => Ok(CurrentSource::Off),
            0b001 => Ok(CurrentSource::C10uA),
            0b010 => Ok(CurrentSource::C50uA),
            0b011 => Ok(CurrentSource::C100uA),
            0b100 => Ok(CurrentSource::C250uA),
            0b101 => Ok(CurrentSource::C500uA),
            0b110 => Ok(CurrentSource::C1000uA),
            0b111 => Ok(CurrentSource::C1500uA),
            _ => Err(()),
        }
    }
}

impl CurrentSource {
    pub fn as_value(&self) -> f32 {
        1e-6 * match self {
            CurrentSource::Off => 0,
            CurrentSource::C10uA => 10,
            CurrentSource::C50uA => 50,
            CurrentSource::C100uA => 100,
            CurrentSource::C250uA => 250,
            CurrentSource::C500uA => 500,
            CurrentSource::C1000uA => 1000,
            CurrentSource::C1500uA => 1500,
        } as f32
    }
}

pub enum IdacMux {
    Disabled = 0b000,
    AIN0 = 0b001,
    AIN1 = 0b010,
    AIN2 = 0b011,
    AIN3 = 0b100,
    REFP = 0b101,
    RefN = 0b110,
    Reserved = 0b111,
}

impl TryFrom<u8> for IdacMux {
    type Error = ();

    fn try_from(value: u8) -> Result<Self, Self::Error> {
        match value {
            0b000 => Ok(IdacMux::Disabled),
            0b001 => Ok(IdacMux::AIN0),
            0b010 => Ok(IdacMux::AIN1),
            0b011 => Ok(IdacMux::AIN2),
            0b100 => Ok(IdacMux::AIN3),
            0b101 => Ok(IdacMux::REFP),
            0b110 => Ok(IdacMux::RefN),
            0b111 => Ok(IdacMux::Reserved),
            _ => Err(()),
        }
    }
}

pub const MUX_REG: u8 = 0x00;
pub const MUX_MASK: u8 = 0b1111_0000;
pub const MUX_SHIFT: u8 = 4;

pub const GAIN_REG: u8 = 0x00;
pub const GAIN_MASK: u8 = 0b0000_1110;
pub const GAIN_SHIFT: u8 = 1;

pub const PGA_REG: u8 = 0x00;
pub const PGA_MASK: u8 = 0b0000_0001;
pub const PGA_SHIFT: u8 = 0;

pub const DR_REG: u8 = 0x01;
pub const DR_MASK: u8 = 0b1110_0000;
pub const DR_SHIFT: u8 = 5;

pub const MODE_REG: u8 = 0x01;
pub const MODE_MASK: u8 = 0b0001_0000;
pub const MODE_SHIFT: u8 = 4;

pub const CM_REG: u8 = 0x01;
pub const CM_MASK: u8 = 0b0000_1000;
pub const CM_SHIFT: u8 = 3;

pub const VREF_REG: u8 = 0x01;
pub const VREF_MASK: u8 = 0b0000_0110;
pub const VREF_SHIFT: u8 = 1;

pub const TS_REG: u8 = 0x01;
pub const TS_MASK: u8 = 0b0000_0001;
pub const TS_SHIFT: u8 = 0;

pub const DRDY_REG: u8 = 0x02;
pub const DRDY_MASK: u8 = 0b1000_0000;
pub const DRDY_SHIFT: u8 = 7;

pub const DCNT_REG: u8 = 0x02;
pub const DCNT_MASK: u8 = 0b0100_0000;
pub const DCNT_SHIFT: u8 = 6;

pub const CRC_REG: u8 = 0x02;
pub const CRC_MASK: u8 = 0b0011_0000;
pub const CRC_SHIFT: u8 = 4;

pub const BCS_REG: u8 = 0x02;
pub const BCS_MASK: u8 = 0b0000_1000;
pub const BCS_SHIFT: u8 = 3;

pub const IDAC_REG: u8 = 0x02;
pub const IDAC_MASK: u8 = 0b0000_0111;
pub const IDAC_SHIFT: u8 = 0;

pub const IMUX1_REG: u8 = 0x03;
pub const IMUX1_MASK: u8 = 0b1110_0000;
pub const IMUX1_SHIFT: u8 = 5;

pub const IMUX2_REG: u8 = 0x03;
pub const IMUX2_MASK: u8 = 0b0001_1100;
pub const IMUX2_SHIFT: u8 = 2;

#[derive(Copy, Clone)]
pub enum SamplingMethod {
    DrdyBit,
    DrdyCnt,
}

pub enum SamplingResult {
    DrdyBit(u32),
    DrdyCnt(u32, u8),
}

impl SamplingResult {
    pub fn data(&self) -> u32 {
        match self {
            SamplingResult::DrdyBit(value) => *value,
            SamplingResult::DrdyCnt(value, _) => *value,
        }
    }
}
