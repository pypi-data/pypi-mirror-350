#[cfg(not(feature = "std"))]
use core::result::Result as CoreResult;
#[cfg(feature = "std")]
use std::result::Result as CoreResult;

use binrw::{binrw, BinRead, BinWrite};

#[binrw]
#[brw(big)]
#[br(import(trargs: TRArgs, erargs: ERArgs))]
#[bw(import(twargs: TWArgs, ewargs: EWArgs))]
#[derive(Debug)]
pub enum Result<
    T: for<'a> BinRead<Args<'a> = TRArgs> + for<'a> BinWrite<Args<'a> = TWArgs>,
    E: for<'a> BinRead<Args<'a> = ERArgs> + for<'a> BinWrite<Args<'a> = EWArgs>,
    TRArgs,
    TWArgs,
    ERArgs,
    EWArgs,
> {
    Ok(
        #[br(args_raw = trargs)]
        #[bw(args_raw = twargs)]
        T,
    ),
    Err(
        #[br(args_raw = erargs)]
        #[bw(args_raw = ewargs)]
        E,
    ),
}

impl<
        T: for<'a> BinRead<Args<'a> = TRArgs> + for<'a> BinWrite<Args<'a> = TWArgs>,
        E: for<'a> BinRead<Args<'a> = ERArgs> + for<'a> BinWrite<Args<'a> = EWArgs>,
        TRArgs,
        TWArgs,
        ERArgs,
        EWArgs,
    > From<CoreResult<T, E>> for Result<T, E, TRArgs, TWArgs, ERArgs, EWArgs>
{
    fn from(result: CoreResult<T, E>) -> Self {
        match result {
            Ok(t) => Self::Ok(t),
            Err(e) => Self::Err(e),
        }
    }
}

impl<
        T: for<'a> BinRead<Args<'a> = TRArgs> + for<'a> BinWrite<Args<'a> = TWArgs>,
        E: for<'a> BinRead<Args<'a> = ERArgs> + for<'a> BinWrite<Args<'a> = EWArgs>,
        TRArgs,
        TWArgs,
        ERArgs,
        EWArgs,
    > Into<CoreResult<T, E>> for Result<T, E, TRArgs, TWArgs, ERArgs, EWArgs>
{
    fn into(self) -> CoreResult<T, E> {
        match self {
            Self::Ok(t) => Ok(t),
            Self::Err(e) => Err(e),
        }
    }
}
