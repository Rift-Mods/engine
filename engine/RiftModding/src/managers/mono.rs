use std::{error, path::Path, fs, ffi::CStr};


use libc::{c_void};
use unity_rs::mono::{types::{MonoMethod, MonoImage, MonoClass,  MonoString, MonoObject}};

use crate::{utils::{files::{mods_dir}},log, err, debug};

pub static mut MONO_PATCH: Option<*mut MonoMethod> = None;

pub fn init() -> Result<(), Box<dyn error::Error>> {
    debug!("test")?;
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
    let path = Path::new(&dir);
    let paths = fs::read_dir(path).unwrap();
    for path in paths {
        if !&path.as_ref().unwrap().path().to_str().unwrap().ends_with(".disabled") {
            let p: *mut c_void =   MonoString::new(&path.as_ref().unwrap().path().to_str().unwrap().to_owned()).unwrap().cast();
            let mut params = vec![p];
            match unsafe { MONO_PATCH } {
                Some(method) => {
                    log!("loading: {:?}", &path.as_ref().unwrap().path().to_str().unwrap())?;
                    let res = MonoMethod::invoke(method, None, Some(&mut params)); // current limitation if it fails it dies cant do anything about it right now
                    match res {
                        Ok(_n) => {
                            log!("loaded: {:?}", &path.unwrap().path().to_str().unwrap())?;
                        }
                        Err(e) => { // never actually gets to here
                            log!("failed loading")?;
                            err!("{:?}", e)?;
                        }
                    }


                }
                None => {
                    err!("No mono patch method")?
                }
            };
        }

    }
    Ok(())
}
