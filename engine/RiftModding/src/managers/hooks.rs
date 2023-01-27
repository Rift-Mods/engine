use std::{ffi::{c_char, c_void}, mem::transmute, error};
use thiserror::Error;
use unity_rs::{mono::{types::{MonoDomain, MonoMethod, MonoObject}}, runtime::{UnityRuntime, Runtime}};

use crate::{internal_failure, utils::{detours::{self}}, managers::{internal_calls, base_asm}};

#[derive(Debug, Error)]
pub enum HookError {
    #[error("Failed to get mono_jit_init_version")]
    MonoJitInitVersion,
    #[error("Failed to get mono_runtime_invoke")]
    MonoRuntimeInvoke,
    #[error("Failed to hook function")]
    HookFunction,
}

type InvokeFnMono = fn(*mut MonoMethod, *mut MonoObject, *mut *mut c_void, *mut *mut MonoObject) -> *mut MonoObject;

type InitFnMono = fn(*const c_char, *const c_char) -> *mut MonoDomain;

static mut MONO_JIT_INIT_ORIGINAL: Option<InitFnMono> = None;
static mut MONO_RUNTIME_INVOKE_ORIGINAL: Option<InvokeFnMono> = None;



pub fn init(runtime: UnityRuntime) -> Result<(), Box<dyn error::Error>> {
    match runtime {
        UnityRuntime::MonoRuntime(mono) => unsafe {
            let func = mono.exports.mono_jit_init_version.ok_or(HookError::MonoJitInitVersion)?;

            let trampoline = detours::hook(*func as usize, mono_jit_init_version_detour as usize).map_err(|_| HookError::HookFunction)?;

            MONO_JIT_INIT_ORIGINAL = Some(transmute(trampoline));

            Ok(())
        }
        _ => {unimplemented!("xd")}
    }
}

fn invoke(runtime: UnityRuntime) -> Result<(), HookError> {
    match runtime {
        UnityRuntime::MonoRuntime(mono) => unsafe {
            let func = mono.exports.mono_runtime_invoke.ok_or(HookError::MonoRuntimeInvoke)?;

            let trampoline = detours::hook(*func as usize, mono_runtime_invoke_detour as usize).map_err(|_| HookError::HookFunction)?;

            MONO_RUNTIME_INVOKE_ORIGINAL = Some(transmute(trampoline));

            Ok(())
        },
        _ => {unimplemented!("xd")}
    }
}

fn mono_jit_init_version_detour(name: *const c_char, version: *const c_char) -> *mut MonoDomain {
    mono_jit_init_version_detour_inner(name, version).unwrap_or_else(|e| {
        internal_failure!("mono_jit_init_version detour failed: {e}");
    })
}

fn mono_runtime_invoke_detour(method: *mut MonoMethod, obj: *mut MonoObject, params: *mut *mut c_void, exc: *mut *mut MonoObject) -> *mut MonoObject {
    mono_runtime_invoke_detour_inner(method, obj, params, exc).unwrap_or_else(|e| {
        internal_failure!("mono_runtime_invoke detour failed: {e}");
    })
}



fn mono_jit_init_version_detour_inner(name: *const c_char, version: *const c_char) -> Result<*mut MonoDomain, Box<dyn std::error::Error>> {
    let trampoline = unsafe {
        MONO_JIT_INIT_ORIGINAL.ok_or_else(|| "mono_jit_init_version trampoline not found")?
    };

    let domain = trampoline(name, version);

    let runtime = Runtime::new()?;

    if let UnityRuntime::MonoRuntime(mono) = &runtime.runtime{
        let func = mono.exports.clone();
        let func = func.mono_jit_init_version.ok_or(HookError::MonoJitInitVersion)?;
        detours::unhook(*func as usize)?;

        let thread = runtime.get_current_thread()?;
        mono.thread_set_main(thread)?;

        if !mono.is_old {
            if let Some(mono_domain_set_config) = &mono.exports.mono_domain_set_config {
                let base_dir = std::env::current_dir()?;
                let base_dir = base_dir.to_str().ok_or("Failed to convert base dir to string")?;
                let base_dir = std::ffi::CString::new(base_dir)?;
                mono_domain_set_config(domain, base_dir.as_ptr(), name);
            }
        }

        internal_calls::init(mono.to_owned())?;
        base_asm::init()?;
        invoke(runtime.runtime)?;
    }



    Ok(domain)
}

fn mono_runtime_invoke_detour_inner(method: *mut MonoMethod, obj: *mut MonoObject, params: *mut *mut c_void, exc: *mut *mut MonoObject) -> Result<*mut MonoObject, Box<dyn std::error::Error>> {
    let trampoline = unsafe {
        MONO_RUNTIME_INVOKE_ORIGINAL.ok_or("mono_runtime_invoke trampoline not found")?
    };

    let result = trampoline(method, obj, params, exc);

    let name = MonoMethod::get_name(method)?;

    let runtime = Runtime::new()?;
    let mono = match &runtime.runtime {
        UnityRuntime::MonoRuntime(mono) => mono,
        _ => return Ok(result),
    };

    if (name.contains("Internal_ActiveSceneChanged") || name.contains("UnityEngine.ISerializationCallbackReceiver.OnAfterSerialize")) ||
        (mono.is_old && (name.contains("Awake") || name.contains("DoSendMouseEvents"))) {
            let func = mono.exports.clone().mono_runtime_invoke.ok_or(HookError::MonoRuntimeInvoke)?;
            detours::unhook(*func as usize)?;
            super::mono::pre_start()?;
        }

    Ok(result)
}
