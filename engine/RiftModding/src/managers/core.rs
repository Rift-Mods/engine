use std::{error::Error};

use unity_rs::runtime::Runtime;

use crate::{utils::log, debug};


use super::hooks;


pub fn init() -> Result<(), Box<dyn Error>> {
    log::init()?;
    debug!("Logging initialized")?;
    hooks::init(
        Runtime::new()?.runtime
    )?;

    Ok(())
}
