from cffi import FFI

import make_cdefs



SOURCE = """
#include <spa/buffer/alloc.h>
#include <spa/buffer/buffer.h>
#include <spa/buffer/meta.h>
#include <spa/buffer/type-info.h>
#include <spa/control/control.h>
#include <spa/control/type-info.h>
#include <spa/debug/buffer.h>
#include <spa/debug/dict.h>
#include <spa/debug/format.h>
#include <spa/debug/mem.h>
#include <spa/debug/node.h>
#include <spa/debug/pod.h>
#include <spa/debug/types.h>
#include <spa/graph/graph.h>
#include <spa/monitor/device.h>
#include <spa/monitor/event.h>
#include <spa/monitor/type-info.h>
#include <spa/monitor/utils.h>
#include <spa/node/command.h>
#include <spa/node/event.h>
#include <spa/node/io.h>
#include <spa/node/keys.h>
#include <spa/node/node.h>
#include <spa/node/type-info.h>
#include <spa/node/utils.h>
#include <spa/param/audio/format-utils.h>
#include <spa/param/audio/format.h>
#include <spa/param/audio/iec958.h>
#include <spa/param/audio/layout.h>
#include <spa/param/audio/raw.h>
#include <spa/param/audio/type-info.h>
#include <spa/param/bluetooth/audio.h>
#include <spa/param/bluetooth/type-info.h>
#include <spa/param/video/chroma.h>
#include <spa/param/video/color.h>
#include <spa/param/video/encoded.h>
#include <spa/param/video/format-utils.h>
#include <spa/param/video/format.h>
#include <spa/param/video/multiview.h>
#include <spa/param/video/raw.h>
#include <spa/param/video/type-info.h>
#include <spa/param/format-utils.h>
#include <spa/param/format.h>
#include <spa/param/latency-utils.h>
#include <spa/param/param.h>
#include <spa/param/profiler.h>
#include <spa/param/props.h>
#include <spa/param/type-info.h>
#include <spa/pod/builder.h>
#include <spa/pod/command.h>
#include <spa/pod/compare.h>
#include <spa/pod/event.h>
#include <spa/pod/filter.h>
#include <spa/pod/iter.h>
#include <spa/pod/parser.h>
#include <spa/pod/pod.h>
#include <spa/pod/vararg.h>
#include <spa/support/cpu.h>
#include <spa/support/dbus.h>
#include <spa/support/i18n.h>
#include <spa/support/log-impl.h>
#include <spa/support/log.h>
#include <spa/support/loop.h>
#include <spa/support/system.h>
#include <spa/support/thread.h>
#include <spa/utils/ansi.h>
#include <spa/utils/defs.h>
#include <spa/utils/dict.h>
#include <spa/utils/hook.h>
#include <spa/utils/json.h>
#include <spa/utils/keys.h>
#include <spa/utils/list.h>
#include <spa/utils/names.h>
#include <spa/utils/result.h>
#include <spa/utils/ringbuffer.h>
#include <spa/utils/string.h>
#include <spa/utils/type-info.h>
#include <spa/utils/type.h>

#include <pipewire/pipewire.h>
"""

# XXX: dynamic version?
LIB = "libpipewire-0.3"


def build():
    CDEF, cbs = make_cdefs.make_cdefs(SOURCE, LIB, exclude_files=[
        "spa/support/plugin.h",
    ], include_macros_integers=[
        "PW_DIRECTION_INPUT",
        "PW_DIRECTION_OUTPUT",
        "SPA_TIME_INVALID",
        "SPA_IDX_INVALID",
        "SPA_ID_INVALID",
        "SPA_NSEC_PER_SEC",
        "SPA_NSEC_PER_MSEC",
        "SPA_NSEC_PER_USEC",
        "SPA_USEC_PER_SEC",
        "SPA_USEC_PER_MSEC",
        "SPA_MSEC_PER_SEC",
        "SPA_DATA_FLAG_READWRITE",
        "SPA_BUFFER_ALLOC_FLAG_INLINE_ALL",
        "SPA_PARAM_INFO_READWRITE",
        "SPA_CPU_FORCE_AUTODETECT",
        "SPA_ASYNC_SEQ_MASK",
        "SPA_ASYNC_MASK",
        "PW_ID_ANY",
        "PW_PERM_RWX",
        "PW_PERM_RWXM",
        "PW_PERM_ALL",
        "PW_PERM_INVALID",
    ], exclude_macros=[
        "SPA_AUDIO_LAYOUT_MPEG_1_0",
        "SPA_AUDIO_LAYOUT_MPEG_2_0",
    ], exclude_funcs=[
        # NOTE: excluded b/c variadic and implemented as macros.
        "spa_log_error",
        "spa_log_warn",
        "spa_log_info",
        "spa_log_debug",
        "spa_log_trace",
        "spa_log_log",
        "spa_log_trace_fp",
        "spa_system_ioctl",
        # NOTE: excluded b/c not exported.
        "pw_mempool_new",
        "pw_mempool_add_listener",
        "pw_mempool_clear",
        "pw_mempool_destroy",
        "pw_mempool_remove_id",
        "pw_data_loop_get_loop",
    ])

    ffi_builder = FFI()
    ffi_builder.cdef(CDEF)
    ffi_builder.set_source_pkgconfig(
        "pipewire._ffi",
        [LIB],
        SOURCE,
    )
    ffi_builder.compile()

    with open("pipewire/_cbs.py", "w") as f:
        f.write("from ._ffi import ffi\n")
        for type_name, group_name, fct_name in cbs:
            f.write(f"@ffi.def_extern()\ndef py_cb_{type_name}_{group_name}_{fct_name}(data, *args):\n    return ffi.from_handle(data)['{fct_name}'](*args)\n")


if __name__ == "__main__":
    build()
