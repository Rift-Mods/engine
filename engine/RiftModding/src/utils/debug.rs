use std::env;
pub fn enabled() -> bool {
    for arg in env::args() {
        if arg == "--debug" {
            return true;
        }
    }
    false
}
