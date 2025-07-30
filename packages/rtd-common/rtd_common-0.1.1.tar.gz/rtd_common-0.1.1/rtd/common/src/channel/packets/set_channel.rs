use binrw::binrw;

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[binrw]
#[brw(big)]
#[derive(Debug, Default, Copy, Clone)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(get_all, set_all))]
pub enum RTDType {
    #[default]
    #[brw(magic(0u8))]
    PT100,
    #[brw(magic(1u8))]
    PT500,
    #[brw(magic(2u8))]
    PT1000,
    #[brw(magic(3u8))]
    Cu10,
    #[brw(magic(4u8))]
    Cu50,
    #[brw(magic(5u8))]
    Cu100,
    #[brw(magic(6u8))]
    Ni100,
    #[brw(magic(7u8))]
    Ni120,
    #[brw(magic(8u8))]
    Ni1000,
}

/// https://www.thermocoupleinfo.com
#[binrw]
#[brw(big)]
#[derive(Debug, Default, Copy, Clone)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(get_all, set_all))]
pub enum TCType {
    #[brw(magic(0u8))]
    E, // -9.835mV to 76.373mV
    #[default]
    #[brw(magic(1u8))]
    J, // -8.095mV to 69.554mV
    #[brw(magic(2u8))]
    K, // -6.458mV to 54.886mV
    #[brw(magic(3u8))]
    N, // -4.345mV to 47.513mV
    #[brw(magic(4u8))]
    R, // -0.226mV to 21.101mV
    #[brw(magic(5u8))]
    S, // -0.236mV to 18.693mV
    #[brw(magic(6u8))]
    T, // -6.258mV to 20.824mV
    #[brw(magic(7u8))]
    B, // 0.0mV to 13.820mV
}

#[binrw]
#[brw(big)]
#[derive(Debug, Copy, Clone)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(get_all, set_all))]
pub enum ChannelType {
    #[brw(magic(0u8))]
    None(),
    #[brw(magic(1u8))]
    RTD(RTDType),
    #[brw(magic(2u8))]
    TC(TCType),
}

impl Default for ChannelType {
    fn default() -> Self {
        ChannelType::RTD(RTDType::default())
    }
}

#[binrw]
#[brw(big)]
#[derive(Default, Debug, Clone, Copy)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(get_all, set_all))]
pub struct ChannelConfig {
    pub channel_type: ChannelType,
    pub max_resistance: f32,
    pub min_resistance: f32,
    pub shunt_resistance: f32,
    pub r_ain0: f32,
}

#[cfg(feature = "pyo3")]
#[pymethods]
impl ChannelConfig {
    #[new]
    pub fn new(
        channel_type: ChannelType,
        max_resistance: f32,
        min_resistance: f32,
        shunt_resistance: f32,
        r_ain0: f32,
    ) -> Self {
        Self {
            channel_type,
            max_resistance,
            min_resistance,
            shunt_resistance,
            r_ain0,
        }
    }
}

#[binrw]
#[derive(Debug, Clone)]
pub struct SetChannelRequest {
    pub channel_config: ChannelConfig,
}

#[binrw]
#[brw(big)]
#[derive(Debug, Clone)]
pub struct SetChannelResponse {
    pub success: u8,
}

#[cfg(all(feature = "pyo3", not(feature = "std")))]
use alloc::vec::Vec;
#[cfg(all(feature = "pyo3", feature = "std"))]
use std::vec::Vec;

#[cfg(feature = "pyo3")]
#[pyfunction]
#[pyo3(name = "set_channel_request")]
pub fn set_channel_py(c_number: usize, c_config: ChannelConfig, id: u32) -> Vec<u8> {
    hal_common::packets::Request::with_id(
        crate::channel::packets::Request::General::<crate::channel::rtd::packets::Request>(
            crate::channel::packets::GeneralRequest::SetChannel(SetChannelRequest {
                channel_config: c_config,
            }),
        ),
        id,
    )
    .into(c_number as u8)
    .as_bytes()
}

#[cfg(feature = "pyo3")]
#[pyfunction]
#[pyo3(name = "sys_reset")]
pub fn sys_reset_py() -> Vec<u8> {
    hal_common::packets::Request::with_id(
        crate::channel::packets::Request::General::<crate::channel::rtd::packets::Request>(
            crate::channel::packets::GeneralRequest::SysReset(),
        ),
        1,
    )
    .into(0)
    .as_bytes()
}

#[cfg(feature = "pyo3")]
pub(crate) fn pymodule(py: Python) -> PyResult<pyo3::Bound<'_, pyo3::types::PyModule>> {
    PyModule::new(py, "set_channel").map(|module| {
        module.add_class::<ChannelConfig>()?;
        module.add_class::<ChannelType>()?;
        module.add_class::<RTDType>()?;
        module.add_class::<TCType>()?;
        Ok(module)
    })?
}
