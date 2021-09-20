from ._ffi_spa import ffi as ffis
from ._ffi_spa import lib as libs
from ._ffi_pipewire import ffi as ffip
from ._ffi_pipewire import lib as libp


# Dynamically updated by poetry-dynamic-versioning.
__version__ = "0.0.0"

__version_pipewire_api__ = ffip.string(libp.PW_API_VERSION).decode()
__version_pipewire_library__ = ffip.string(libp.pw_get_library_version()).decode()
__version_pipewire__ = f"{libp.PW_MAJOR}.{libp.PW_MINOR}.{libp.PW_MICRO}"


for ffi, tps in (
    (ffis, (
        ("spa_device", (
            ("event", ("info", "result", "event", "object_info")),
        )),
        ("spa_graph_node", (
            ("callback", ("process", "reuse_buffer")),
        )),
        ("spa_node", (
            ("callback", ("ready", "reuse_buffer", "xrun")),
            ("event", ("info", "port_info", "result", "event")),
        )),
        ("spa_loop_control", (
            ("hook", ("before", "after")),
        )),
    )),
    (ffip, (
        ("pw_client", (
            ("event", ("info", "permissions")),
        )),
        ("pw_context", (
            ("event", ("destroy", "free", "check_access", "global_added", "global_removed")),
        )),
        ("pw_core", (
            ("event", ("info", "done", "ping", "error", "remove_id", "bound_id", "add_mem", "remove_mem")),
        )),
        ("pw_registry", (
            ("event", ("global", "global_remove")),
        )),
        ("pw_data_loop", (
            ("event", ("destroy",)),
        )),
        ("pw_device", (
            ("event", ("info", "param")),
        )),
        ("pw_factory", (
            ("event", ("info",)),
        )),
        ("pw_filter", (
            ("event", ("destroy", "state_changed", "io_changed", "param_changed", "add_buffer", "remove_buffer", "process", "drained")),
        )),
        ("pw_link", (
            ("event", ("info",)),
        )),
        ("pw_main_loop", (
            ("event", ("destroy",)),
        )),
        ("pw_mempool", (
            ("event", ("destroy", "added", "removed")),
        )),
        ("pw_module", (
            ("event", ("info",)),
        )),
        ("pw_node", (
            ("event", ("info", "param")),
        )),
        ("pw_port", (
            ("event", ("info", "param")),
        )),
        ("pw_protocol", (
            ("event", ("destroy",)),
        )),
        ("pw_proxy", (
            ("event", ("destroy", "bound", "removed", "done", "error")),
        )),
        ("pw_stream", (
            ("event", ("destroy", "state_changed", "control_info", "io_changed", "param_changed", "add_buffer", "remove_buffer", "process", "drained")),
        )),
        ("pw_thread_loop", (
            ("event", ("destroy",)),
        )),
    )),
):
    for tp_name, groups in tps:
        for group_name, fcts in groups:
            for fct_name in fcts:
                globals()[f"py_cb_{tp_name}_{group_name}_{fct_name}"] = ffi.def_extern(
                    name=f"py_cb_{tp_name}_{group_name}_{fct_name}",
                )(
                    lambda data, *args, fct_name=fct_name: ffi.from_handle(data)[fct_name](*args),
                )
