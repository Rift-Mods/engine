use std::{error, path::Path};


use libc::{c_void};
use unity_rs::mono::{types::{MonoMethod, MonoImage, MonoClass,  MonoString}};

use crate::{utils::files::{mods_dir}};

pub static mut MONO_PATCH: Option<*mut MonoMethod> = None;

pub fn init() -> Result<(), Box<dyn error::Error>> {

    let image = MonoImage::open("RiftModding/Patcher/Patcher.dll")?;
    let class = MonoImage::get_class(image, "", "Patcher")?;
    let patch_method = MonoClass::get_method(class, "Patch", 1)?;
    unsafe {
        MONO_PATCH= Some(patch_method);
    }
    Ok(())
}

pub fn pre_start() -> Result<(), Box<dyn error::Error>> {
    let dir = mods_dir().unwrap();
    let path = Path::new(&dir).join("test.dll");
    let p: *mut c_void =   MonoString::new(path.to_str().unwrap()).unwrap().to_owned().cast();
    let mut params = vec![p];
    match unsafe { MONO_PATCH } {
        Some(method) => {
            let res = MonoMethod::invoke(method, None, Some(&mut params));
            match res {
                Ok(_) => Ok(()),
                Err(e) => Err(e)
            }


        },
        None => {
            Err("Mono prestart method not found".into())
        }
    }
}
