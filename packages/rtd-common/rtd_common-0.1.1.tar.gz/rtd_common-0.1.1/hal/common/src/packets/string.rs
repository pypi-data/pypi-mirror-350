#[cfg(not(feature = "std"))]
use alloc::string::ToString;
#[cfg(not(feature = "std"))]
use alloc::{boxed::Box, string::String as AllocString, vec};
#[cfg(not(feature = "std"))]
use core::{
    fmt::{Debug, Formatter, Result as FormatResult},
    marker::PhantomData,
    ops::{Deref, DerefMut},
};

#[cfg(feature = "std")]
use std::string::ToString;
#[cfg(feature = "std")]
use std::{boxed::Box, string::String as AllocString, vec};
#[cfg(feature = "std")]
use std::{
    fmt::{Debug, Formatter, Result as FormatResult},
    marker::PhantomData,
    ops::{Deref, DerefMut},
};

use binrw::{BinRead, BinWrite};
use num_traits::AsPrimitive;

#[derive(Clone)]
pub struct String<L: AsPrimitive<usize>>(AllocString, PhantomData<L>);

impl<L: AsPrimitive<usize>> Deref for String<L> {
    type Target = AllocString;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
impl<L: AsPrimitive<usize>> DerefMut for String<L> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}
impl<L: AsPrimitive<usize>> String<L> {
    pub fn to_string(self) -> AllocString {
        self.0
    }
}

impl<L: AsPrimitive<usize>> From<AllocString> for String<L> {
    fn from(s: AllocString) -> Self {
        Self(s, PhantomData)
    }
}

impl<L: AsPrimitive<usize>> Debug for String<L> {
    fn fmt(&self, f: &mut Formatter<'_>) -> FormatResult {
        self.0.fmt(f)
    }
}

impl<L: AsPrimitive<usize>> BinRead for String<L> {
    type Args<'a> = (L,);

    fn read_options<R: binrw::io::Read + binrw::io::Seek>(
        reader: &mut R,
        _endian: binrw::Endian,
        args: Self::Args<'_>,
    ) -> binrw::BinResult<Self> {
        let mut data = vec![0u8; args.0.as_()];
        reader.read_exact(&mut data)?;
        AllocString::from_utf8(data)
            .map(|v| Self(v, PhantomData))
            .map_err(|_| binrw::Error::Custom {
                pos: 0,
                err: Box::new("Invalid UTF-8".to_string()),
            })
    }
}

impl<L: AsPrimitive<usize>> BinWrite for String<L> {
    type Args<'a> = ();

    fn write_options<W: binrw::io::Write>(
        &self,
        writer: &mut W,
        _endian: binrw::Endian,
        _args: Self::Args<'_>,
    ) -> binrw::BinResult<()> {
        writer.write_all(self.0.as_bytes())?;
        Ok(())
    }
}
