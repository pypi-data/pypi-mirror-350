#![cfg_attr(not(feature = "std"), no_std)]

#[cfg(not(feature = "std"))]
extern crate alloc;

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

pub mod packets;

#[cfg(feature = "pyo3")]
#[pymodule(name = "hal_common")]
fn pymodule(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    let submodule = &packets::pymodule(py)?;
    py.import("sys")?
        .getattr("modules")?
        .set_item("hal_common.packets", submodule)?;
    m.add_submodule(submodule)?;
    Ok(())
}
