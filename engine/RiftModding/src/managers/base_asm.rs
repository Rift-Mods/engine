use std::error::Error;

pub fn init() -> Result<(), Box<dyn Error>> {
    super::mono::init()?;
    Ok(())
}
