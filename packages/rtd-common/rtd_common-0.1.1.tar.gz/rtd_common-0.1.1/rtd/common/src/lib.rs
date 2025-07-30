#![cfg_attr(not(feature = "std"), no_std)]

#[cfg(not(feature = "std"))]
extern crate alloc;

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

pub mod ads122c04;
pub mod channel;
pub mod tca6416a;

#[cfg(feature = "pyo3")]
use channel::{
    packets::set_channel::set_channel_py, packets::set_channel::sys_reset_py,
    rtd::packets::set_temperature::set_temperature_py,
};

#[cfg(feature = "pyo3")]
#[pymodule(name = "rtd_common")]
fn pymodule(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    let submodule = &channel::pymodule(py)?;
    py.import("sys")?
        .getattr("modules")?
        .set_item("rtd_common.channel", submodule)?; // CHECK HERE
    m.add_submodule(submodule)?;
    m.add_function(wrap_pyfunction!(set_channel_py, m)?)?;
    m.add_function(wrap_pyfunction!(sys_reset_py, m)?)?;
    m.add_function(wrap_pyfunction!(set_temperature_py, m)?)?;
    Ok(())
}
