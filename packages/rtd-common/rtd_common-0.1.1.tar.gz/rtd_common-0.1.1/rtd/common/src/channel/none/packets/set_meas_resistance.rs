use binrw::binrw;

use crate::ads122c04::Gain;

#[binrw]
#[brw(big)]
#[derive(Debug)]
pub struct SetMeasResistanceRequest {
    pub resistance: f32,
    pub regulate: u32,
}

#[binrw]
#[brw(big)]
#[derive(Debug)]
pub struct SetMeasResistanceResponse {
    pub pins: u16,
    pub target: f32,
    pub resistance: f32,
    pub voltage_s1: f32,
    pub voltage_s2: f32,
    pub current: f32,
    pub gain_s1: Gain,
    pub gain_s2: Gain,
    pub gain_shunt: Gain,
}
