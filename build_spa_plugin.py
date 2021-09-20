from cffi import FFI

import build_spa


SOURCE = ""

CDEF = ""

# forwards
# enums/structs/types
# macros
# fcts
# vars
# py fcts

# XXX: SPA_SUPPORT_INIT(type, data)
SOURCE += """
#include <spa/support/plugin.h>
"""
CDEF += """
struct spa_handle {
    uint32_t version;
    int (*get_interface) (struct spa_handle *handle, const char *type, void **interface);
    int (*clear) (struct spa_handle *handle);
};
struct spa_interface_info {
    const char *type;
};
struct spa_support {
    const char *type;
    void *data;
};
struct spa_handle_factory {
    uint32_t version;
    const char *name;
    const struct spa_dict *info;
    size_t (*get_size) (const struct spa_handle_factory *factory, const struct spa_dict *params);
    int (*init) (const struct spa_handle_factory *factory, struct spa_handle *handle, const struct spa_dict *info, const struct spa_support *support, uint32_t n_support);
    int (*enum_interface_info) (const struct spa_handle_factory *factory, const struct spa_interface_info **info, uint32_t *index);
};
typedef ... spa_handle_factory_enum_func_t;

static const int SPA_VERSION_HANDLE;
static const int SPA_VERSION_HANDLE_FACTORY;
static char * const SPA_HANDLE_FACTORY_ENUM_FUNC_NAME;
static char * const SPA_KEY_FACTORY_NAME;
static char * const SPA_KEY_FACTORY_AUTHOR;
static char * const SPA_KEY_FACTORY_DESCRIPTION;
static char * const SPA_KEY_FACTORY_USAGE;
static char * const SPA_KEY_LIBRARY_NAME;
int spa_handle_get_interface(struct spa_handle *handle, const char *type, void **interface);
int spa_handle_clear(struct spa_handle *handle);
size_t spa_handle_factory_get_size(const struct spa_handle_factory *factory, const struct spa_dict *params);
int spa_handle_factory_init(const struct spa_handle_factory *factory, struct spa_handle *handle, const struct spa_dict *info, const struct spa_support *support, uint32_t n_support);
int spa_handle_factory_enum_interface_info(const struct spa_handle_factory *factory, const struct spa_interface_info **info, uint32_t *index);

void *spa_support_find(const struct spa_support *support, uint32_t n_support, const char *type);
int spa_handle_factory_enum(const struct spa_handle_factory **factory, uint32_t *index);
"""



ffi_builder = FFI()
ffi_builder.include(build_spa.ffi_builder)
# XXX: cffi requires that *all* elements included via ffi_builder.include(...) are actually reached in the includer's source... ugly way, just include the whole list of SPA headers...
#      see also https://foss.heptapod.net/pypy/cffi/-/issues/420
SOURCE += build_spa.SOURCE
ffi_builder.cdef(CDEF)


def build(name, init_py_filepath):
    build_spa.build()
    ffi_builder.set_source_pkgconfig(
        name,
        # XXX: dynamic version?
        ["libspa-0.2"],
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
