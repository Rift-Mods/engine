use std::{
    error::{Error},
    ffi::{c_void}, mem::transmute
};
use unity_rs::{mono::{Mono}};

use crate::{utils::{detours}};

static mut MONO: Option<Mono> = None;

pub fn init(mono: Mono) -> Result<(), Box<dyn Error>> {
    unsafe {
        MONO = Some(mono);
    }
    Ok(())
}
pub fn NativeHookAttach(target: *mut *mut c_void, detour: *mut c_void) {
    unsafe {
        match detours::hook(*target as usize, detour as usize) {
            Ok(res) => *target = transmute(res),
            Err(_e) => {}
        };
    }
}

pub fn NativeHookDetach(target: *mut *mut c_void, _detour: *mut c_void)  {
    unsafe {
        detours::unhook(*target as usize).unwrap_or_else(|_e| {

        });
    }
}
