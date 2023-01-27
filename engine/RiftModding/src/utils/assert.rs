#[macro_export]
macro_rules! internal_failure {
    ($($arg:tt)*) => {{
        let msg = &format_args!($($arg)*).to_string();

        let _ = msgbox::create("Internal Failure", msg, msgbox::IconType::Error);
        std::process::exit(-1);
    }};
}
