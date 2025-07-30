use binrw::binrw;

#[binrw]
#[derive(Debug)]
pub struct SetTemperatureRequest {
    pub temperature: f32,
}

#[binrw]
#[brw(big)]
#[derive(Debug)]
pub struct SetTemperatureResponse {
    pub success: u8,
}
