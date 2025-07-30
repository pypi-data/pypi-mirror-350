use binrw::binrw;

use crate::ads122c04::Gain;

#[binrw]
#[brw(big)]
#[derive(Debug)]
pub struct SetMeasPinsRequest {
    pub pins: u16,
    pub iterations: u32,
}

#[binrw]
#[brw(big)]
#[derive(Debug)]
pub struct SetMeasPinsResponse {
    pub pins: u16,
    pub resistance: f32,
    pub voltage_s1: f32,
    pub voltage_s2: f32,
    pub current: f32,
    pub gain_s1: Gain,
    pub gain_s2: Gain,
    pub gain_shunt: Gain,
}
