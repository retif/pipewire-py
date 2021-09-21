import pipewire



def make_client_handle(fct_name, extra_data):
    def cb(info):
        print(f"client: id:{info.id}")
        print("\tprops:")
        # XXX: spa_dict_for_each not available.
        for n in range(info.props.n_items):
            print(f'\t\t{pipewire.ffi.string(info.props.items[n].key).decode()}: "{pipewire.ffi.string(info.props.items[n].value).decode()}"')

        pipewire.lib.pw_main_loop_quit(extra_data["loop"])

    return pipewire.ffi.new_handle({fct_name: cb})


def make_registry_handle(fct_name, extra_data):
    def cb(id, permissions, type, version, props):
        if extra_data["client"] is not None:
            return

        if pipewire.ffi.string(type).decode() == pipewire.ffi.string(pipewire.lib.PW_TYPE_INTERFACE_Client).decode():
            extra_data["client"] = pipewire.lib.pw_registry_bind(
                extra_data["registry"],
                id,
                type,
                pipewire.lib.PW_VERSION_CLIENT,
                0,
            )
            pipewire.lib.pw_client_add_listener(
                extra_data["client"],
                extra_data["client_listener"],
                extra_data["client_events"],
                extra_data["cb_handle_client"],
            )

    return pipewire.ffi.new_handle({fct_name: cb})


def main():
    registry_listener = pipewire.ffi.new("struct spa_hook *")
    registry_events = pipewire.ffi.new("struct pw_registry_events *")
    registry_events.version = pipewire.lib.PW_VERSION_REGISTRY_EVENTS
    setattr(registry_events, "global", pipewire.lib.py_cb_pw_registry_event_global)

    client_listener = pipewire.ffi.new("struct spa_hook *")
    client_events = pipewire.ffi.new("struct pw_client_events *")
    client_events.version = pipewire.lib.PW_VERSION_CLIENT_EVENTS
    setattr(client_events, "info", pipewire.lib.py_cb_pw_client_event_info)

    pipewire.lib.pw_init(pipewire.ffi.NULL, pipewire.ffi.NULL)

    loop = pipewire.lib.pw_main_loop_new(pipewire.ffi.NULL)
    context = pipewire.lib.pw_context_new(pipewire.lib.pw_main_loop_get_loop(loop), pipewire.ffi.NULL, 0)

    core = pipewire.lib.pw_context_connect(context, pipewire.ffi.NULL, 0)

    registry = pipewire.lib.pw_core_get_registry(core, pipewire.lib.PW_VERSION_REGISTRY, 0)

    cb_data = {"loop": loop, "registry": registry, "client_listener": client_listener, "client_events": client_events, "client": None}
    cb_handle_client = make_client_handle("info", cb_data)
    cb_data["cb_handle_client"] = cb_handle_client
    cb_handle = make_registry_handle("global", cb_data)

    pipewire.lib.pw_registry_add_listener(registry, registry_listener, registry_events, cb_handle)

    pipewire.lib.pw_main_loop_run(loop)

    pipewire.lib.pw_proxy_destroy(pipewire.ffi.cast("struct pw_proxy *", cb_data["client"]))
    pipewire.lib.pw_proxy_destroy(pipewire.ffi.cast("struct pw_proxy *", registry))
    pipewire.lib.pw_core_disconnect(core)
    pipewire.lib.pw_context_destroy(context)
    pipewire.lib.pw_main_loop_destroy(loop)


if __name__ == "__main__":
    main()
