pub mod none;
pub mod packets;
pub mod rtd;
pub mod tc;

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[cfg(feature = "pyo3")]
pub(crate) fn pymodule(py: Python) -> PyResult<pyo3::Bound<'_, pyo3::types::PyModule>> {
    PyModule::new(py, "channel").map(|module| {
        let submodule = &packets::pymodule(py)?;
        py.import("sys")?
            .getattr("modules")?
            .set_item("rtd_common.channel.packets", submodule)?;
        module.add_submodule(submodule)?;
        let submodule = &rtd::pymodule(py)?;
        py.import("sys")?
            .getattr("modules")?
            .set_item("rtd_common.channel.rtd", submodule)?;
        module.add_submodule(submodule)?;
        Ok(module)
    })?
}
