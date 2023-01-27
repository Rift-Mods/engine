use std::{error::Error};

use unity_rs::runtime::Runtime;

use super::hooks;

pub fn version() -> &'static str {
    "0.0.1"
}


pub fn init() -> Result<(), Box<dyn Error>> {

    hooks::init(
        Runtime::new()?.runtime
    )?;

    Ok(())
}
