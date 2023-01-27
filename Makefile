linux:
	@cargo build
	@rm -rf "/home/nikkuss/Desktop/123123/RiftModding.so"
	@mv target/debug/libBootstrap.so "/home/nikkuss/Desktop/123123/RiftModding/"

windows:
	@cargo xwin build --target x86_64-pc-windows-msvc
	@dotnet build engine/Patcher
	@rm -rf "/home/nikkuss/Desktop/123123/RiftModding/Patcher"
	@rm -rf "/home/nikkuss/Desktop/123123/RiftModding/RiftModding.dll"
	@rm -rf "/home/nikkuss/Desktop/123123/version.dll"
	@mkdir -p /home/nikkuss/Desktop/123123/RiftModding/Patcher
	@mv engine/Patcher/bin/Debug/net4.8/Patcher.dll "/home/nikkuss/Desktop/123123/RiftModding/Patcher"
	@mv engine/Patcher/bin/Debug/net4.8/0Harmony.dll "/home/nikkuss/Desktop/123123/RiftModding/Patcher"
	@mv target/x86_64-pc-windows-msvc/debug/RiftModding.dll "/home/nikkuss/Desktop/123123/RiftModding/RiftModding.dll"
	@mv target/x86_64-pc-windows-msvc/debug/version.dll "/home/nikkuss/Desktop/123123/version.dll"
