use std::path::PathBuf;

pub fn get_bootstrap_path(base_path: &PathBuf) -> Result<PathBuf, Box<dyn std::error::Error>> {
    let win_default = ["RiftModding", "RiftModding"];
    let mut path = base_path.clone();
    let args: Vec<String> = std::env::args().collect();
    for i in 0..args.len() {
        if args[i] == "--riftmodding.basepath" {
            if i + 1 >= args.len() {
                return Err("No path specified for --riftmodding.basepath".into());
            }
            path = PathBuf::from(&args[i + 1]);
            break;
        }
    }

    let mut windows_path = path.clone();

    windows_path.extend(win_default.iter());

    let windows_path = windows_path.with_extension(std::env::consts::DLL_EXTENSION);

    if windows_path.exists() {
        Ok(windows_path)
    } else {
        Err("Failed to find bootstrap".into())
    }
}
