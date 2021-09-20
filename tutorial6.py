import pipewire



def make_client_handle(fct_name, extra_data):
    def cb(info):
        print(f"client: id:{info.id}")
        print("\tprops:")
        # XXX: spa_dict_for_each not available.
        for n in range(info.props.n_items):
            print(f'\t\t{pipewire.ffip.string(info.props.items[n].key).decode()}: "{pipewire.ffip.string(info.props.items[n].value).decode()}"')

        pipewire.libp.pw_main_loop_quit(extra_data["loop"])

    return pipewire.ffip.new_handle({fct_name: cb})


def make_registry_handle(fct_name, extra_data):
    def cb(id, permissions, type, version, props):
        if extra_data["client"] is not None:
            return

        if pipewire.ffip.string(type).decode() == pipewire.ffip.string(pipewire.libp.PW_TYPE_INTERFACE_Client).decode():
            extra_data["client"] = pipewire.libp.pw_registry_bind(
                extra_data["registry"],
                id,
                type,
                pipewire.libp.PW_VERSION_CLIENT,
                0,
            )
            pipewire.libp.pw_client_add_listener(
                extra_data["client"],
                extra_data["client_listener"],
                extra_data["client_events"],
                extra_data["cb_handle_client"],
            )

    return pipewire.ffip.new_handle({fct_name: cb})


def main():
    registry_listener = pipewire.ffip.new("struct spa_hook *")
    registry_events = pipewire.ffip.new("struct pw_registry_events *")
    registry_events.version = pipewire.libp.PW_VERSION_REGISTRY_EVENTS
    setattr(registry_events, "global", pipewire.libp.py_cb_pw_registry_event_global)

    client_listener = pipewire.ffip.new("struct spa_hook *")
    client_events = pipewire.ffip.new("struct pw_client_events *")
    client_events.version = pipewire.libp.PW_VERSION_CLIENT_EVENTS
    setattr(client_events, "info", pipewire.libp.py_cb_pw_client_event_info)

    pipewire.libp.pw_init(pipewire.ffip.NULL, pipewire.ffip.NULL)

    loop = pipewire.libp.pw_main_loop_new(pipewire.ffip.NULL)
    context = pipewire.libp.pw_context_new(pipewire.libp.pw_main_loop_get_loop(loop), pipewire.ffip.NULL, 0)

    core = pipewire.libp.pw_context_connect(context, pipewire.ffip.NULL, 0)

    registry = pipewire.libp.pw_core_get_registry(core, pipewire.libp.PW_VERSION_REGISTRY, 0)

    cb_data = {"loop": loop, "registry": registry, "client_listener": client_listener, "client_events": client_events, "client": None}
    cb_handle_client = make_client_handle("info", cb_data)
    cb_data["cb_handle_client"] = cb_handle_client
    cb_handle = make_registry_handle("global", cb_data)

    pipewire.libp.pw_registry_add_listener(registry, registry_listener, registry_events, cb_handle)

    pipewire.libp.pw_main_loop_run(loop)

    pipewire.libp.pw_proxy_destroy(pipewire.ffip.cast("struct pw_proxy *", cb_data["client"]))
    pipewire.libp.pw_proxy_destroy(pipewire.ffip.cast("struct pw_proxy *", registry))
    pipewire.libp.pw_core_disconnect(core)
    pipewire.libp.pw_context_destroy(context)
    pipewire.libp.pw_main_loop_destroy(loop)


if __name__ == "__main__":
    main()
