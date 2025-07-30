use binrw::binrw;

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[binrw]
#[brw(big)]
#[derive(Debug, Clone)]
pub struct SetTemperatureRequest {
    pub temperature: f32,
}

#[binrw]
#[brw(big)]
#[derive(Debug, Clone)]
pub struct SetTemperatureResponse {
    pub success: u8,
}

#[cfg(all(feature = "pyo3", not(feature = "std")))]
use alloc::vec::Vec;
#[cfg(all(feature = "pyo3", feature = "std"))]
use std::vec::Vec;

#[cfg(feature = "pyo3")]
#[pyfunction]
#[pyo3(name = "set_temperature_request")]
pub fn set_temperature_py(c_number: usize, temperature_value: f32, id: u32) -> Vec<u8> {
    hal_common::packets::Request::with_id(
        crate::channel::packets::Request::Impl(
            crate::channel::rtd::packets::Request::SetTemperature(
                SetTemperatureRequest { temperature: temperature_value },
            ),
        ),
        id,
    )
    .into(c_number as u8)
    .as_bytes()
}

#[cfg(feature = "pyo3")]
pub(crate) fn pymodule(py: Python) -> PyResult<pyo3::Bound<'_, pyo3::types::PyModule>> {
    PyModule::new(py, "set_temperature").map(|module| {
        Ok(module)
    })?
}