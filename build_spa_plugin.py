from cffi import FFI

import make_cdefs



SOURCE = """
#include <spa/support/plugin.h>
"""

# XXX: dynamic version?
LIB = "libspa-0.2"


def build(name, init_py_filepath):
    CDEF, cbs = make_cdefs.make_cdefs(SOURCE, LIB)

    ffi_builder = FFI()
    ffi_builder.cdef(CDEF)

    ffi_builder.set_source_pkgconfig(
        name,
        [LIB],
        SOURCE,
    )
    ffi_builder.embedding_init_code(open(init_py_filepath).read())
    ffi_builder.compile()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        build(*sys.argv[1:])
    else:
        build("test_spa_plugin", "test_spa_plugin.py")
