import pipewire



def main():
    pipewire.lib.pw_init(pipewire.ffi.NULL, pipewire.ffi.NULL)

    print(f"pipewire version {pipewire.__version__}")
    print(f"Compiled with libpipewire {pipewire.__version_pipewire__}, API {pipewire.__version_pipewire_api__}")
    print(f"Linked with libpipewire {pipewire.__version_pipewire_library__}")


if __name__ == "__main__":
    main()
