import pipewire



def make_core_handle(fct_name, extra_data):
    def cb(id, seq):
        if id == pipewire.libp.PW_ID_CORE and seq == extra_data["pending"]:
            extra_data["done"] = True
            pipewire.libp.pw_main_loop_quit(extra_data["loop"])

    return pipewire.ffip.new_handle({fct_name: cb})


def roundtrip(core, loop):
    core_listener = pipewire.ffip.new("struct spa_hook *")
    core_events = pipewire.ffip.new("struct pw_core_events *")
    core_events.version = pipewire.libp.PW_VERSION_CORE_EVENTS
    core_events.done = pipewire.libp.py_cb_pw_core_event_done

    cb_data = {"loop": loop, "done": False}
    cb_handle = make_core_handle("done", cb_data)

    pipewire.libp.pw_core_add_listener(core, core_listener, core_events, cb_handle)

    pending = pipewire.libp.pw_core_sync(core, pipewire.libp.PW_ID_CORE, 0)
    cb_data["pending"] = pending

    while not cb_data["done"]:
        pipewire.libp.pw_main_loop_run(loop)

    pipewire.libs.spa_hook_remove(core_listener)


def make_registry_handle(fct_name):
    def cb(id, permissions, type, version, props):
        print(f"object: id:{id} type:{pipewire.ffip.string(type).decode()}/{version}")

    return pipewire.ffip.new_handle({fct_name: cb})


def main():
    registry_listener = pipewire.ffip.new("struct spa_hook *")
    registry_events = pipewire.ffip.new("struct pw_registry_events *")
    registry_events.version = pipewire.libp.PW_VERSION_REGISTRY_EVENTS
    setattr(registry_events, "global", pipewire.libp.py_cb_pw_registry_event_global)

    pipewire.libp.pw_init(pipewire.ffip.NULL, pipewire.ffip.NULL)

    loop = pipewire.libp.pw_main_loop_new(pipewire.ffip.NULL)
    context = pipewire.libp.pw_context_new(pipewire.libp.pw_main_loop_get_loop(loop), pipewire.ffip.NULL, 0)

    core = pipewire.libp.pw_context_connect(context, pipewire.ffip.NULL, 0)

    registry = pipewire.libp.pw_core_get_registry(core, pipewire.libp.PW_VERSION_REGISTRY, 0)

    cb_handle = make_registry_handle("global")

    pipewire.libp.pw_registry_add_listener(registry, registry_listener, registry_events, cb_handle)

    roundtrip(core, loop)

    pipewire.libp.pw_proxy_destroy(pipewire.ffip.cast("struct pw_proxy *", registry))
    pipewire.libp.pw_core_disconnect(core)
    pipewire.libp.pw_context_destroy(context)
    pipewire.libp.pw_main_loop_destroy(loop)


if __name__ == "__main__":
    main()
