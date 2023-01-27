//! Contains various utilities for files

use std::{error::Error, path::PathBuf, env, fs};

use unity_rs::runtime::{Runtime, UnityRuntime};

/// evaluates wether or not a path contains non-ASCII characters.
pub fn check_ascii(path: &PathBuf) -> Result<(), Box<dyn Error>> {
    let base_string = path.to_str().ok_or("Failed to turn PathBuf into a string!")?;

    if base_string.is_ascii() {
        Ok(())
    } else {
        Err("The base directory path contains non-ASCII characters!")?
    }
}


#[macro_export]
macro_rules! join_dll_path {
    //take two arguments, a PathBuf and a file name
    ($path:expr, $file:expr) => {
        //join the path and the file name
        $path.join($file)
        //add the correct extension
        .with_extension(std::env::consts::DLL_EXTENSION)
    };
}

/// gets the game's base directory.
pub fn base_dir() -> Result<PathBuf, Box<dyn Error>> {
    let app_path = env::current_exe()?;

    let base_path = app_path.parent().ok_or("Failed to get the base path!")?;

    match base_path.exists() {
        true => Ok(base_path.to_path_buf()),
        false => Err("The base path does not exist!")?,
    }
}

pub fn managed_dir() -> Result<PathBuf, Box<dyn Error>> {
    let file_path = std::env::current_exe()?;

    let file_name = file_path.file_stem()
        .ok_or_else(|| "Data Path not found!")?
        .to_str()
        .ok_or_else(|| "Data Path not found!")?;

    let base_folder = file_path.parent()
        .ok_or_else(|| "Data Path not found!")?;

    let managed_path = base_folder.join(format!("{}_Data", file_name)).join("Managed");

    match managed_path.exists() {
        true => Ok(managed_path),
        false => {
            Err("No Managed Dir")?
        }
    }
}

pub fn riftmods_dir() -> Result<PathBuf, Box<dyn Error>> {
    let riftmod_path = base_dir()?.join("RiftModding");

    match riftmod_path.exists() {
        true => Ok(riftmod_path),
        false => Err("RiftWorld Folder does not exist!")?,
    }
}

pub fn mods_dir() -> Result<PathBuf, Box<dyn Error>> {
    let riftmod_path = riftmods_dir()?;
    let mods_path = riftmod_path.join("mods");
    match mods_path.exists() {
        true => Ok(mods_path),
        false => {
            fs::create_dir_all(&mods_path).expect("coudlnt make mods path");
            Ok(mods_path)
        }
    }

}

pub fn runtime_dir() -> Result<PathBuf, Box<dyn Error>> {
    let runtime_dir = riftmods_dir()?;

    let runtime = Runtime::new()?;

    match runtime.runtime {
        UnityRuntime::MonoRuntime(_) => Ok(runtime_dir.join("net35")),
        UnityRuntime::Il2Cpp(_) => Ok(runtime_dir.join("net6")),
    }
}
