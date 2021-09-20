import pipewire



def main():
    pipewire.libp.pw_init(pipewire.ffip.NULL, pipewire.ffip.NULL)

    print(f"pipewire version {pipewire.__version__}")
    print(f"Compiled with libpipewire {pipewire.__version_pipewire__}, API {pipewire.__version_pipewire_api__}")
    print(f"Linked with libpipewire {pipewire.__version_pipewire_library__}")


if __name__ == "__main__":
    main()
