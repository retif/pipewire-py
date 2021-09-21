import pipewire



def make_core_handle(fct_name, extra_data):
    def cb(id, seq):
        if id == pipewire.lib.PW_ID_CORE and seq == extra_data["pending"]:
            extra_data["done"] = True
            pipewire.lib.pw_main_loop_quit(extra_data["loop"])

    return pipewire.ffi.new_handle({fct_name: cb})


def roundtrip(core, loop):
    core_listener = pipewire.ffi.new("struct spa_hook *")
    core_events = pipewire.ffi.new("struct pw_core_events *")
    core_events.version = pipewire.lib.PW_VERSION_CORE_EVENTS
    core_events.done = pipewire.lib.py_cb_pw_core_event_done

    cb_data = {"loop": loop, "done": False}
    cb_handle = make_core_handle("done", cb_data)

    pipewire.lib.pw_core_add_listener(core, core_listener, core_events, cb_handle)

    pending = pipewire.lib.pw_core_sync(core, pipewire.lib.PW_ID_CORE, 0)
    cb_data["pending"] = pending

    while not cb_data["done"]:
        pipewire.lib.pw_main_loop_run(loop)

    pipewire.lib.spa_hook_remove(core_listener)


def make_registry_handle(fct_name):
    def cb(id, permissions, type, version, props):
        print(f"object: id:{id} type:{pipewire.ffi.string(type).decode()}/{version}")

    return pipewire.ffi.new_handle({fct_name: cb})


def main():
    registry_listener = pipewire.ffi.new("struct spa_hook *")
    registry_events = pipewire.ffi.new("struct pw_registry_events *")
    registry_events.version = pipewire.lib.PW_VERSION_REGISTRY_EVENTS
    setattr(registry_events, "global", pipewire.lib.py_cb_pw_registry_event_global)

    pipewire.lib.pw_init(pipewire.ffi.NULL, pipewire.ffi.NULL)

    loop = pipewire.lib.pw_main_loop_new(pipewire.ffi.NULL)
    context = pipewire.lib.pw_context_new(pipewire.lib.pw_main_loop_get_loop(loop), pipewire.ffi.NULL, 0)

    core = pipewire.lib.pw_context_connect(context, pipewire.ffi.NULL, 0)

    registry = pipewire.lib.pw_core_get_registry(core, pipewire.lib.PW_VERSION_REGISTRY, 0)

    cb_handle = make_registry_handle("global")

    pipewire.lib.pw_registry_add_listener(registry, registry_listener, registry_events, cb_handle)

    roundtrip(core, loop)

    pipewire.lib.pw_proxy_destroy(pipewire.ffi.cast("struct pw_proxy *", registry))
    pipewire.lib.pw_core_disconnect(core)
    pipewire.lib.pw_context_destroy(context)
    pipewire.lib.pw_main_loop_destroy(loop)


if __name__ == "__main__":
    main()
