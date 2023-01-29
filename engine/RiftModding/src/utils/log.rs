use std::{
    io::Write,
    path::PathBuf, error,
};

use thiserror::Error;

use super::{debug, files};

#[derive(Error, Debug)]
pub enum LogError {
    /// the log file could not be deleted
    #[error("Failed to delete the old log file")]
    FailedToDeleteOldLog,

    /// the log file could not be written to
    #[error("Failed to write to log file")]
    FailedToWriteToLog,

    /// the base path could not be fetched
    #[error("Failed to fetch base path")]
    FailedToGetBasePath,
}

/// gets the path to the log file
fn log_path() -> Result<PathBuf, Box<dyn error::Error>> {
    let base_path = files::base_dir()?;
    let log_path = base_path.join("RiftModding/Latest.log");

    Ok(log_path)
}


pub fn init() -> Result<(), Box<dyn error::Error>> {
    let log_path = log_path().map_err(|_| LogError::FailedToGetBasePath)?;

    if log_path.exists() {
        std::fs::remove_file(&log_path).map_err(|_| LogError::FailedToDeleteOldLog)?;
    }
    Ok(())
}


#[derive(Debug)]
pub enum LogLevel {
    Info,
    Warning,
    Error,
    Debug,
}
fn write(msg: &str) -> Result<(), Box<dyn error::Error>> {
    let log_path = log_path().map_err(|_| LogError::FailedToGetBasePath)?;
    let mut file = std::fs::OpenOptions::new()
        .write(true)
        .append(true)
        .create(true)
        .open(&log_path)
        .map_err(|_| LogError::FailedToWriteToLog)?;

    let message = format!("{}\r\n", msg);

    file.write_all(message.as_bytes())
        .map_err(|_| LogError::FailedToWriteToLog)?;

    Ok(())
}

/// logs to console and file, should not be used, use the log! macro instead
pub fn log_console_file(level: LogLevel, message: &str) -> Result<(), Box<LogError>> {
    match level {
        LogLevel::Info => {
            let file_string = format!(
                "[{}] {}",
                timestamp(),
                message
            );
            write(&file_string).map_err(|_| LogError::FailedToWriteToLog)?;
        }
        LogLevel::Warning => {
            let file_string = format!(
                "[{}] [WARNING] {}",
                timestamp(),
                message
            );
            write(&file_string).map_err(|_| LogError::FailedToWriteToLog)?;
        }
        LogLevel::Error => {
            let log_string = format!(
                "[{}] [ERROR] {}",
                timestamp(),
                message
            );
            write(&log_string).map_err(|_| LogError::FailedToWriteToLog)?;
        }
        LogLevel::Debug => {
            if !debug::enabled() {
                return Ok(());
            }
            let file_string = format!(
                "[{}] [DEBUG] {}",
                timestamp(),
                message
            );

            write(&file_string).map_err(|_| LogError::FailedToWriteToLog)?;
        }
    }

    Ok(())
}

fn timestamp() -> String {
    let now = chrono::Local::now();
    let time = now.time();

    time.format("%H:%M:%S.%3f").to_string()
}

#[macro_export]
macro_rules! log {
    //case 1: empty
    () => {
        $crate::utils::log::log_console_file($crate::utils::log::LogLevel::Info, "")
    };

    //case 2: single argument
    ($msg:expr) => {
        $crate::utils::log::log_console_file($crate::utils::log::LogLevel::Info, $msg)
    };

    //case 3: multiple arguments
    ($($arg:tt)*) => {{
        let msg = &format_args!($($arg)*).to_string();
        $crate::utils::log::log_console_file($crate::utils::log::LogLevel::Info, msg)
    }};
}


#[macro_export]
macro_rules! warn {
    //case 1: empty
    () => {
        $crate::utils::log::log_console_file($crate::utils::log::LogLevel::Warning, "")
    };

    //case 2: single argument
    ($msg:expr) => {
        $crate::utils::log::log_console_file($crate::utils::log::LogLevel::Warning, $msg)
    };

    //case 3: multiple arguments
    ($($arg:tt)*) => {{
        let msg = &format_args!($($arg)*).to_string();
        $crate::utils::log::log_console_file($crate::utils::log::LogLevel::Warning, msg)
    }};
}

#[macro_export]
macro_rules! err {
    //case 1: empty
    () => {
        $crate::utils::log::log_console_file($crate::utils::log::LogLevel::Error, "")
    };

    //case 2: single argument
    ($msg:expr) => {
        $crate::utils::log::log_console_file($crate::utils::log::LogLevel::Error, $msg)
    };

    //case 3: multiple arguments
    ($($arg:tt)*) => {{
        let msg = &format_args!($($arg)*).to_string();
        $crate::utils::log::log_console_file($crate::utils::log::LogLevel::Error, msg)
    }};
}

#[macro_export]
macro_rules! debug {
    //case 1: empty
    () => {
        $crate::utils::log::log_console_file($crate::utils::log::LogLevel::Debug, "")
    };

    //case 2: single argument
    ($msg:expr) => {
        $crate::utils::log::log_console_file($crate::utils::log::LogLevel::Debug, $msg)
    };

    //case 3: multiple arguments
    ($($arg:tt)*) => {{
        let msg = &format_args!($($arg)*).to_string();
        $crate::utils::log::log_console_file($crate::utils::log::LogLevel::Debug, msg)
    }};
}

#[macro_export]
macro_rules! cstr {
    ($s:expr) => {
        std::ffi::CString::new($s)?.as_ptr()
    };

    ($($arg:tt)*) => {
       std::ffi::CString::new(format!($($arg)*))?.as_ptr()
    };
}
