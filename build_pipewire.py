from cffi import FFI

import build_spa


SOURCE = """
#include <pipewire/pipewire.h>
"""

CDEF = ""

# forwards
# enums/structs/types
# macros
# fcts
# vars
# py fcts

# XXX: >0.3.34: struct pw_(...)_info *pw_(client|core|device|factory|link|module|node|port)_info_merge(struct pw_client_info *info, const struct pw_client_info *update, bool reset);
#               91f1b44499f4cc41c7b4dd3630b27b009d5bdc95

# XXX: macros
# array.h
CDEF += """
struct pw_array {
    void *data;
    size_t size;
    size_t alloc;
    size_t extend;
};

void pw_array_init(struct pw_array *arr, size_t extend);
void pw_array_clear(struct pw_array *arr);
void pw_array_reset(struct pw_array *arr);
int pw_array_ensure_size(struct pw_array *arr, size_t size);
void *pw_array_add(struct pw_array *arr, size_t size);
void *pw_array_add_fixed(struct pw_array *arr, size_t size);
"""

# buffers.h
CDEF += """
struct pw_buffers {
    struct pw_memblock *mem;
    struct spa_buffer **buffers;
    uint32_t n_buffers;
    uint32_t flags;
};

static const int PW_BUFFERS_FLAG_NONE;
static const int PW_BUFFERS_FLAG_NO_MEM;
static const int PW_BUFFERS_FLAG_SHARED;
static const int PW_BUFFERS_FLAG_DYNAMIC;

int pw_buffers_negotiate(struct pw_context *context, uint32_t flags, struct spa_node *outnode, uint32_t out_port_id, struct spa_node *innode, uint32_t in_port_id, struct pw_buffers *result);
void pw_buffers_clear(struct pw_buffers *buffers);
"""

# client.h
CDEF += """
struct pw_client_info {
    uint32_t id;
    uint64_t change_mask;
    struct spa_dict *props;
};
struct pw_client_events {
    uint32_t version;
    void (*info) (void *object, const struct pw_client_info *info);
    void (*permissions) (void *object, uint32_t index, uint32_t n_permissions, const struct pw_permission *permissions);
};
struct pw_client_methods {
    uint32_t version;
    int (*add_listener) (void *object, struct spa_hook *listener, const struct pw_client_events *events, void *data);
    int (*error) (void *object, uint32_t id, int res, const char *message);
    int (*update_properties) (void *object, const struct spa_dict *props);
    int (*get_permissions) (void *object, uint32_t index, uint32_t num);
    int (*update_permissions) (void *object, uint32_t n_permissions, const struct pw_permission *permissions);
};

static char * const PW_TYPE_INTERFACE_Client;
static const int PW_VERSION_CLIENT;
static const int PW_ID_CLIENT;
static const int PW_CLIENT_EVENT_INFO;
static const int PW_CLIENT_EVENT_PERMISSIONS;
static const int PW_CLIENT_EVENT_NUM;
static const int PW_VERSION_CLIENT_EVENTS;
static const int PW_CLIENT_METHOD_ADD_LISTENER;
static const int PW_CLIENT_METHOD_ERROR;
static const int PW_CLIENT_METHOD_UPDATE_PROPERTIES;
static const int PW_CLIENT_METHOD_GET_PERMISSIONS;
static const int PW_CLIENT_METHOD_UPDATE_PERMISSIONS;
static const int PW_CLIENT_METHOD_NUM;
static const int PW_VERSION_CLIENT_METHODS;
int pw_client_add_listener(struct pw_client *c, struct spa_hook *listener, const struct pw_client_events *events, void *data);
int pw_client_error(struct pw_client *c, uint32_t id, int res, const char *message);
int pw_client_update_properties(struct pw_client *c, const struct spa_dict *props);
int pw_client_get_permissions(struct pw_client *c, uint32_t index, uint32_t num);
int pw_client_update_permissions(struct pw_client *c, uint32_t n_permissions, const struct pw_permission *permissions);

struct pw_client_info *pw_client_info_update(struct pw_client_info *info, const struct pw_client_info *update);
void pw_client_info_free(struct pw_client_info *info);

extern "Python" {
    void py_cb_pw_client_event_info(void *data, const struct pw_client_info *info);
    void py_cb_pw_client_event_permissions(void *data, uint32_t index, uint32_t n_permissions, const struct pw_permission *permissions);
}
"""

# context.h
CDEF += """
struct pw_context_events {
    uint32_t version;
    void (*destroy) (void *data);
    void (*free) (void *data);
    void (*check_access) (void *data, struct pw_impl_client *client);
    void (*global_added) (void *data, struct pw_global *global);
    void (*global_removed) (void *data, struct pw_global *global);
};
struct pw_export_type {
    struct spa_list link;
    const char *type;
    struct pw_proxy * (*func) (struct pw_core *core, const char *type, const struct spa_dict *props, void *object, size_t user_data_size);
};

static const int PW_VERSION_CONTEXT_EVENTS;

struct pw_context *pw_context_new(struct pw_loop *main_loop, struct pw_properties *props, size_t user_data_size);
void pw_context_destroy(struct pw_context *context);
void *pw_context_get_user_data(struct pw_context *context);
void pw_context_add_listener(struct pw_context *context, struct spa_hook *listener, const struct pw_context_events *events, void *data);
const struct pw_properties *pw_context_get_properties(struct pw_context *context);
int pw_context_update_properties(struct pw_context *context, const struct spa_dict *dict);
const char *pw_context_get_conf_section(struct pw_context *context, const char *section);
const struct spa_support *pw_context_get_support(struct pw_context *context, uint32_t *n_support);
struct pw_loop *pw_context_get_main_loop(struct pw_context *context);
struct pw_work_queue *pw_context_get_work_queue(struct pw_context *context);
int pw_context_for_each_global(struct pw_context *context, int (*callback) (void *data, struct pw_global *global), void *data);
struct pw_global *pw_context_find_global(struct pw_context *context, uint32_t id);
int pw_context_add_spa_lib(struct pw_context *context, const char *factory_regex, const char *lib);
const char *pw_context_find_spa_lib(struct pw_context *context, const char *factory_name);
struct spa_handle *pw_context_load_spa_handle(struct pw_context *context, const char *factory_name, const struct spa_dict *info);
int pw_context_register_export_type(struct pw_context *context, struct pw_export_type *type);
const struct pw_export_type *pw_context_find_export_type(struct pw_context *context, const char *type);
int pw_context_set_object(struct pw_context *context, const char *type, void *value);
void *pw_context_get_object(struct pw_context *context, const char *type);

extern "Python" {
    void py_cb_pw_context_event_destroy(void *data);
    void py_cb_pw_context_event_free(void *data);
    void py_cb_pw_context_event_check_access(void *data, struct pw_impl_client *client);
    void py_cb_pw_context_event_global_added(void *data, struct pw_global *global);
    void py_cb_pw_context_event_global_removed(void *data, struct pw_global *global);
}
"""

# core.h
CDEF += """
struct pw_core_info {
    uint32_t id;
    uint32_t cookie;
    const char *user_name;
    const char *host_name;
    const char *version;
    const char *name;
    uint64_t change_mask;
    struct spa_dict *props;
};
struct pw_core_events {
    uint32_t version;
    void (*info) (void *object, const struct pw_core_info *info);
    void (*done) (void *object, uint32_t id, int seq);
    void (*ping) (void *object, uint32_t id, int seq);
    void (*error) (void *object, uint32_t id, int seq, int res, const char *message);
    void (*remove_id) (void *object, uint32_t id);
    void (*bound_id) (void *object, uint32_t id, uint32_t global_id);
    void (*add_mem) (void *object, uint32_t id, uint32_t type, int fd, uint32_t flags);
    void (*remove_mem) (void *object, uint32_t id);
};
struct pw_core_methods {
    uint32_t version;
    int (*add_listener) (void *object, struct spa_hook *listener, const struct pw_core_events *events, void *data);
    int (*hello) (void *object, uint32_t version);
    int (*sync) (void *object, uint32_t id, int seq);
    int (*pong) (void *object, uint32_t id, int seq);
    int (*error) (void *object, uint32_t id, int seq, int res, const char *message);
    struct pw_registry * (*get_registry) (void *object, uint32_t version, size_t user_data_size);
    void * (*create_object) (void *object, const char *factory_name, const char *type, uint32_t version, const struct spa_dict *props, size_t user_data_size);
    int (*destroy) (void *object, void *proxy);
};
struct pw_registry_events {
    uint32_t version;
    void (*global) (void *object, uint32_t id, uint32_t permissions, const char *type, uint32_t version, const struct spa_dict *props);
    void (*global_remove) (void *object, uint32_t id);
};
struct pw_registry_methods {
    uint32_t version;
    int (*add_listener) (void *object, struct spa_hook *listener, const struct pw_registry_events *events, void *data);
    void * (*bind) (void *object, uint32_t id, const char *type, uint32_t version, size_t use_data_size);
    int (*destroy) (void *object, uint32_t id);
};

static char * const PW_TYPE_INTERFACE_Core;
static char * const PW_TYPE_INTERFACE_Registry;
static const int PW_VERSION_CORE;
static const int PW_VERSION_REGISTRY;
static char * const PW_DEFAULT_REMOTE;
static const int PW_ID_CORE;
static const uint32_t PW_ID_ANY;
static const int PW_CORE_CHANGE_MASK_PROPS;
static const int PW_CORE_CHANGE_MASK_ALL;
static const int PW_CORE_EVENT_INFO;
static const int PW_CORE_EVENT_DONE;
static const int PW_CORE_EVENT_PING;
static const int PW_CORE_EVENT_ERROR;
static const int PW_CORE_EVENT_REMOVE_ID;
static const int PW_CORE_EVENT_BOUND_ID;
static const int PW_CORE_EVENT_ADD_MEM;
static const int PW_CORE_EVENT_REMOVE_MEM;
static const int PW_CORE_EVENT_NUM;
static const int PW_VERSION_CORE_EVENTS;
static const int PW_CORE_METHOD_ADD_LISTENER;
static const int PW_CORE_METHOD_HELLO;
static const int PW_CORE_METHOD_SYNC;
static const int PW_CORE_METHOD_PONG;
static const int PW_CORE_METHOD_ERROR;
static const int PW_CORE_METHOD_GET_REGISTRY;
static const int PW_CORE_METHOD_CREATE_OBJECT;
static const int PW_CORE_METHOD_DESTROY;
static const int PW_CORE_METHOD_NUM;
static const int PW_VERSION_CORE_METHODS;
int pw_core_add_listener(struct pw_core *c, struct spa_hook *listener, const struct pw_core_events *events, void *data);
int pw_core_hello(struct pw_core *c, uint32_t version);
int pw_core_sync(struct pw_core *c, uint32_t id, int seq);
int pw_core_pong(struct pw_core *c, uint32_t id, int seq);
int pw_core_error(struct pw_core *c, uint32_t id, int seq, int res, const char *message);
int pw_core_destroy(struct pw_core *c, void *proxy);
static const int PW_REGISTRY_EVENT_GLOBAL;
static const int PW_REGISTRY_EVENT_GLOBAL_REMOVE;
static const int PW_REGISTRY_EVENT_NUM;
static const int PW_VERSION_REGISTRY_EVENTS;
static const int PW_REGISTRY_METHOD_ADD_LISTENER;
static const int PW_REGISTRY_METHOD_BIND;
static const int PW_REGISTRY_METHOD_DESTROY;
static const int PW_REGISTRY_METHOD_NUM;
static const int PW_VERSION_REGISTRY_METHODS;
int pw_registry_add_listener(struct pw_registry *p, struct spa_hook *listener, const struct pw_registry_events *events, void *data);
int pw_registry_destroy(struct pw_registry *p, uint32_t id);

struct pw_core_info *pw_core_info_update(struct pw_core_info *info, const struct pw_core_info *update);
void pw_core_info_free(struct pw_core_info *info);
struct pw_registry *pw_core_get_registry(struct pw_core *core, uint32_t version, size_t user_data_size);
void *pw_core_create_object(struct pw_core *core, const char *factory_name, const char *type, uint32_t version, const struct spa_dict *props, size_t user_data_size);
void *pw_registry_bind(struct pw_registry *registry, uint32_t id, const char *type, uint32_t version, size_t user_data_size);
struct pw_core *pw_context_connect(struct pw_context *context, struct pw_properties *properties, size_t user_data_size);
struct pw_core *pw_context_connect_fd(struct pw_context *context, int fd, struct pw_properties *properties, size_t user_data_size);
struct pw_core *pw_context_connect_self(struct pw_context *context, struct pw_properties *properties, size_t user_data_size);
int pw_core_steal_fd(struct pw_core *core);
int pw_core_set_paused(struct pw_core *core, bool paused);
int pw_core_disconnect(struct pw_core *core);
void *pw_core_get_user_data(struct pw_core *core);
struct pw_client *pw_core_get_client(struct pw_core *core);
struct pw_context *pw_core_get_context(struct pw_core *core);
const struct pw_properties *pw_core_get_properties(struct pw_core *core);
int pw_core_update_properties(struct pw_core *core, const struct spa_dict *dict);
struct pw_mempool *pw_core_get_mempool(struct pw_core *core);
struct pw_proxy *pw_core_find_proxy(struct pw_core *core, uint32_t id);
struct pw_proxy *pw_core_export(struct pw_core *core, const char *type, const struct spa_dict *props, void *object, size_t user_data_size);

extern "Python" {
    void py_cb_pw_core_event_info(void *data, const struct pw_core_info *info);
    void py_cb_pw_core_event_done(void *data, uint32_t id, int seq);
    void py_cb_pw_core_event_ping(void *data, uint32_t id, int seq);
    void py_cb_pw_core_event_error(void *data, uint32_t id, int seq, int res, const char *message);
    void py_cb_pw_core_event_remove_id(void *data, uint32_t id);
    void py_cb_pw_core_event_bound_id(void *data, uint32_t id, uint32_t global_id);
    void py_cb_pw_core_event_add_mem(void *data, uint32_t id, uint32_t type, int fd, uint32_t flags);
    void py_cb_pw_core_event_remove_mem(void *data, uint32_t id);
    void py_cb_pw_registry_event_global(void *data, uint32_t id, uint32_t permissions, const char *type, uint32_t version, const struct spa_dict *props);
    void py_cb_pw_registry_event_global_remove(void *data, uint32_t id);
}
"""

# NOTE: for some reason, some functions are not exported:
#       struct pw_loop *pw_data_loop_get_loop(struct pw_data_loop *loop);
# data-loop.h
CDEF += """
struct pw_data_loop_events {
    uint32_t version;
    void (*destroy) (void *data);
};

static const int PW_VERSION_DATA_LOOP_EVENTS;

struct pw_data_loop *pw_data_loop_new(const struct spa_dict *props);
void pw_data_loop_add_listener(struct pw_data_loop *loop, struct spa_hook *listener, const struct pw_data_loop_events *events, void *data);
int pw_data_loop_wait(struct pw_data_loop *loop, int timeout);
void pw_data_loop_exit(struct pw_data_loop *loop);
void pw_data_loop_destroy(struct pw_data_loop *loop);
int pw_data_loop_start(struct pw_data_loop *loop);
int pw_data_loop_stop(struct pw_data_loop *loop);
bool pw_data_loop_in_thread(struct pw_data_loop *loop);
struct spa_thread *pw_data_loop_get_thread(struct pw_data_loop *loop);
int pw_data_loop_invoke(struct pw_data_loop *loop, spa_invoke_func_t func, uint32_t seq, const void *data, size_t size, bool block, void *user_data);

extern "Python" {
    void py_cb_pw_data_loop_event_destroy(void *data);
}
"""

# device.h
CDEF += """
struct pw_device_info {
    uint32_t id;
    uint64_t change_mask;
    struct spa_dict *props;
    struct spa_param_info *params;
    uint32_t n_params;
};
struct pw_device_events {
    uint32_t version;
    void (*info) (void *object, const struct pw_device_info *info);
    void (*param) (void *object, int seq, uint32_t id, uint32_t index, uint32_t next, const struct spa_pod *param);
};
struct pw_device_methods {
    uint32_t version;
    int (*add_listener) (void *object, struct spa_hook *listener, const struct pw_device_events *events, void *data);
    int (*subscribe_params) (void *object, uint32_t *ids, uint32_t n_ids);
    int (*enum_params) (void *object, int seq, uint32_t id, uint32_t start, uint32_t num, const struct spa_pod *filter);
    int (*set_param) (void *object, uint32_t id, uint32_t flags, const struct spa_pod *param);
};

static char * const PW_TYPE_INTERFACE_Device;
static const int PW_VERSION_DEVICE;
static const int PW_DEVICE_CHANGE_MASK_PROPS;
static const int PW_DEVICE_CHANGE_MASK_PARAMS;
static const int PW_DEVICE_CHANGE_MASK_ALL;
static const int PW_DEVICE_EVENT_INFO;
static const int PW_DEVICE_EVENT_PARAM;
static const int PW_DEVICE_EVENT_NUM;
static const int PW_VERSION_DEVICE_EVENTS;
static const int PW_DEVICE_METHOD_ADD_LISTENER;
static const int PW_DEVICE_METHOD_SUBSCRIBE_PARAMS;
static const int PW_DEVICE_METHOD_ENUM_PARAMS;
static const int PW_DEVICE_METHOD_SET_PARAM;
static const int PW_DEVICE_METHOD_NUM;
static const int PW_VERSION_DEVICE_METHODS;
int pw_device_add_listener(struct pw_device *c, struct spa_hook *listener, const struct pw_device_events *events, void *data);
int pw_device_subscribe_params(struct pw_device *c, uint32_t *ids, uint32_t n_ids);
int pw_device_enum_params(struct pw_device *c, int seq, uint32_t id, uint32_t start, uint32_t num, const struct spa_pod *filter);
int pw_device_set_param(struct pw_device *c, uint32_t id, uint32_t flags, const struct spa_pod *param);

struct pw_device_info *pw_device_info_update(struct pw_device_info *info, const struct pw_device_info *update);
void pw_device_info_free(struct pw_device_info *info);

extern "Python" {
    void py_cb_pw_device_event_info(void *data, const struct pw_device_info *info);
    void py_cb_pw_device_event_param(void *data, int seq, uint32_t id, uint32_t index, uint32_t next, const struct spa_pod *param);
}
"""

# factory.h
CDEF += """
struct pw_factory_info {
    uint32_t id;
    const char *name;
    const char *type;
    uint32_t version;
    uint64_t change_mask;
    struct spa_dict *props;
};
struct pw_factory_events {
    uint32_t version;
    void (*info) (void *object, const struct pw_factory_info *info);
};
struct pw_factory_methods {
    uint32_t version;
    int (*add_listener) (void *object, struct spa_hook *listener, const struct pw_factory_events *events, void *data);
};

static char * const PW_TYPE_INTERFACE_Factory;
static const int PW_VERSION_FACTORY;
static const int PW_FACTORY_CHANGE_MASK_PROPS;
static const int PW_FACTORY_CHANGE_MASK_ALL;
static const int PW_FACTORY_EVENT_INFO;
static const int PW_FACTORY_EVENT_NUM;
static const int PW_VERSION_FACTORY_EVENTS;
static const int PW_FACTORY_METHOD_ADD_LISTENER;
static const int PW_FACTORY_METHOD_NUM;
int pw_factory_add_listener(struct pw_factory *c, struct spa_hook *listener, const struct pw_factory_events *events, void *data);

struct pw_factory_info *pw_factory_info_update(struct pw_factory_info *info, const struct pw_factory_info *update);
void pw_factory_info_free(struct pw_factory_info *info);

extern "Python" {
    void py_cb_pw_factory_event_info(void *data, const struct pw_factory_info *info);
}
"""

# NOTE: enum pw_direction is actually defined in port.h, but needs to be {}-declared on the first mention.
# XXX: SPA_PRINTF_FUNC
# filter.h
CDEF += """
enum pw_direction {
    PW_DIRECTION_INPUT,
    PW_DIRECTION_OUTPUT,
};

enum pw_filter_state {
    PW_FILTER_STATE_ERROR,
    PW_FILTER_STATE_UNCONNECTED,
    PW_FILTER_STATE_CONNECTING,
    PW_FILTER_STATE_PAUSED,
    PW_FILTER_STATE_STREAMING,
};
struct pw_filter_events {
    uint32_t version;
    void (*destroy) (void *data);
    void (*state_changed) (void *data, enum pw_filter_state old, enum pw_filter_state state, const char *error);
    void (*io_changed) (void *data, void *port_data, uint32_t id, void *area, uint32_t size);
    void (*param_changed) (void *data, void *port_data, uint32_t id, const struct spa_pod *param);
    void (*add_buffer) (void *data, void *port_data, struct pw_buffer *buffer);
    void (*remove_buffer) (void *data, void *port_data, struct pw_buffer *buffer);
    void (*process) (void *data, struct spa_io_position *position);
    void (*drained) (void *data);
};
enum pw_filter_flags {
    PW_FILTER_FLAG_NONE,
    PW_FILTER_FLAG_INACTIVE,
    PW_FILTER_FLAG_DRIVER,
    PW_FILTER_FLAG_RT_PROCESS,
    PW_FILTER_FLAG_CUSTOM_LATENCY,
};
enum pw_filter_port_flags {
    PW_FILTER_PORT_FLAG_NONE,
    PW_FILTER_PORT_FLAG_MAP_BUFFERS,
    PW_FILTER_PORT_FLAG_ALLOC_BUFFERS,
};

static const int PW_VERSION_FILTER_EVENTS;

const char *pw_filter_state_as_string(enum pw_filter_state state);
struct pw_filter *pw_filter_new(struct pw_core *core, const char *name, struct pw_properties *props);
struct pw_filter *pw_filter_new_simple(struct pw_loop *loop, const char *name, struct pw_properties *props, const struct pw_filter_events *events, void *data);
void pw_filter_destroy(struct pw_filter *filter);
void pw_filter_add_listener(struct pw_filter *filter, struct spa_hook *listener, const struct pw_filter_events *events, void *data);
enum pw_filter_state pw_filter_get_state(struct pw_filter *filter, const char **error);
const char *pw_filter_get_name(struct pw_filter *filter);
struct pw_core *pw_filter_get_core(struct pw_filter *filter);
int pw_filter_connect(struct pw_filter *filter, enum pw_filter_flags flags, const struct spa_pod **params, uint32_t n_params);
uint32_t pw_filter_get_node_id(struct pw_filter *filter);
int pw_filter_disconnect(struct pw_filter *filter);
void *pw_filter_add_port(struct pw_filter *filter, enum pw_direction direction, enum pw_filter_port_flags flags, size_t port_data_size, struct pw_properties *props, const struct spa_pod **params, uint32_t n_params);
int pw_filter_remove_port(void *port_data);
const struct pw_properties *pw_filter_get_properties(struct pw_filter *filter, void *port_data);
int pw_filter_update_properties(struct pw_filter *filter, void *port_data, const struct spa_dict *dict);
int pw_filter_set_error(struct pw_filter *filter, int res, const char *error, ...);
int pw_filter_update_params(struct pw_filter *filter, void *port_data, const struct spa_pod **params, uint32_t n_params);
int pw_filter_get_time(struct pw_filter *filter, struct pw_time *time);
struct pw_buffer *pw_filter_dequeue_buffer(void *port_data);
int pw_filter_queue_buffer(void *port_data, struct pw_buffer *buffer);
void *pw_filter_get_dsp_buffer(void *port_data, uint32_t n_samples);
int pw_filter_set_active(struct pw_filter *filter, bool active);
int pw_filter_flush(struct pw_filter *filter, bool drain);

extern "Python" {
    void py_cb_pw_filter_event_destroy(void *data);
    void py_cb_pw_filter_event_state_changed(void *data, enum pw_filter_state old, enum pw_filter_state state, const char *error);
    void py_cb_pw_filter_event_io_changed(void *data, void *port_data, uint32_t id, void *area, uint32_t size);
    void py_cb_pw_filter_event_param_changed(void *data, void *port_data, uint32_t id, const struct spa_pod *param);
    void py_cb_pw_filter_event_add_buffer(void *data, void *port_data, struct pw_buffer *buffer);
    void py_cb_pw_filter_event_remove_buffer(void *data, void *port_data, struct pw_buffer *buffer);
    void py_cb_pw_filter_event_process(void *data, struct spa_io_position *position);
    void py_cb_pw_filter_event_drained(void *data);
}
"""

# XXX: what about PW_KEY_PRIORITY_MASTER (deprecated)?
# keys.h
CDEF += """
static char * const PW_KEY_PROTOCOL;
static char * const PW_KEY_ACCESS;
static char * const PW_KEY_CLIENT_ACCESS;
static char * const PW_KEY_SEC_PID;
static char * const PW_KEY_SEC_UID;
static char * const PW_KEY_SEC_GID;
static char * const PW_KEY_SEC_LABEL;
static char * const PW_KEY_LIBRARY_NAME_SYSTEM;
static char * const PW_KEY_LIBRARY_NAME_LOOP;
static char * const PW_KEY_LIBRARY_NAME_DBUS;
static char * const PW_KEY_OBJECT_PATH;
static char * const PW_KEY_OBJECT_ID;
static char * const PW_KEY_OBJECT_LINGER;
static char * const PW_KEY_OBJECT_REGISTER;
static char * const PW_KEY_CONFIG_PREFIX;
static char * const PW_KEY_CONFIG_NAME;
static char * const PW_KEY_CONTEXT_PROFILE_MODULES;
static char * const PW_KEY_USER_NAME;
static char * const PW_KEY_HOST_NAME;
static char * const PW_KEY_CORE_NAME;
static char * const PW_KEY_CORE_VERSION;
static char * const PW_KEY_CORE_DAEMON;
static char * const PW_KEY_CORE_ID;
static char * const PW_KEY_CORE_MONITORS;
static char * const PW_KEY_CPU_MAX_ALIGN;
static char * const PW_KEY_CPU_CORES;
static char * const PW_KEY_PRIORITY_SESSION;
static char * const PW_KEY_PRIORITY_DRIVER;
static char * const PW_KEY_REMOTE_NAME;
static char * const PW_KEY_REMOTE_INTENTION;
static char * const PW_KEY_APP_NAME;
static char * const PW_KEY_APP_ID;
static char * const PW_KEY_APP_VERSION;
static char * const PW_KEY_APP_ICON;
static char * const PW_KEY_APP_ICON_NAME;
static char * const PW_KEY_APP_LANGUAGE;
static char * const PW_KEY_APP_PROCESS_ID;
static char * const PW_KEY_APP_PROCESS_BINARY;
static char * const PW_KEY_APP_PROCESS_USER;
static char * const PW_KEY_APP_PROCESS_HOST;
static char * const PW_KEY_APP_PROCESS_MACHINE_ID;
static char * const PW_KEY_APP_PROCESS_SESSION_ID;
static char * const PW_KEY_WINDOW_X11_DISPLAY;
static char * const PW_KEY_CLIENT_ID;
static char * const PW_KEY_CLIENT_NAME;
static char * const PW_KEY_CLIENT_API;
static char * const PW_KEY_NODE_ID;
static char * const PW_KEY_NODE_NAME;
static char * const PW_KEY_NODE_NICK;
static char * const PW_KEY_NODE_DESCRIPTION;
static char * const PW_KEY_NODE_PLUGGED;
static char * const PW_KEY_NODE_SESSION;
static char * const PW_KEY_NODE_GROUP;
static char * const PW_KEY_NODE_EXCLUSIVE;
static char * const PW_KEY_NODE_AUTOCONNECT;
static char * const PW_KEY_NODE_TARGET;
static char * const PW_KEY_NODE_LATENCY;
static char * const PW_KEY_NODE_MAX_LATENCY;
static char * const PW_KEY_NODE_LOCK_QUANTUM;
static char * const PW_KEY_NODE_RATE;
static char * const PW_KEY_NODE_LOCK_RATE;
static char * const PW_KEY_NODE_DONT_RECONNECT;
static char * const PW_KEY_NODE_ALWAYS_PROCESS;
static char * const PW_KEY_NODE_WANT_DRIVER;
static char * const PW_KEY_NODE_PAUSE_ON_IDLE;
static char * const PW_KEY_NODE_CACHE_PARAMS;
static char * const PW_KEY_NODE_DRIVER;
static char * const PW_KEY_NODE_STREAM;
static char * const PW_KEY_NODE_VIRTUAL;
static char * const PW_KEY_NODE_PASSIVE;
static char * const PW_KEY_NODE_LINK_GROUP;
static char * const PW_KEY_PORT_ID;
static char * const PW_KEY_PORT_NAME;
static char * const PW_KEY_PORT_DIRECTION;
static char * const PW_KEY_PORT_ALIAS;
static char * const PW_KEY_PORT_PHYSICAL;
static char * const PW_KEY_PORT_TERMINAL;
static char * const PW_KEY_PORT_CONTROL;
static char * const PW_KEY_PORT_MONITOR;
static char * const PW_KEY_PORT_CACHE_PARAMS;
static char * const PW_KEY_PORT_EXTRA;
static char * const PW_KEY_LINK_ID;
static char * const PW_KEY_LINK_INPUT_NODE;
static char * const PW_KEY_LINK_INPUT_PORT;
static char * const PW_KEY_LINK_OUTPUT_NODE;
static char * const PW_KEY_LINK_OUTPUT_PORT;
static char * const PW_KEY_LINK_PASSIVE;
static char * const PW_KEY_LINK_FEEDBACK;
static char * const PW_KEY_DEVICE_ID;
static char * const PW_KEY_DEVICE_NAME;
static char * const PW_KEY_DEVICE_PLUGGED;
static char * const PW_KEY_DEVICE_NICK;
static char * const PW_KEY_DEVICE_STRING;
static char * const PW_KEY_DEVICE_API;
static char * const PW_KEY_DEVICE_DESCRIPTION;
static char * const PW_KEY_DEVICE_BUS_PATH;
static char * const PW_KEY_DEVICE_SERIAL;
static char * const PW_KEY_DEVICE_VENDOR_ID;
static char * const PW_KEY_DEVICE_VENDOR_NAME;
static char * const PW_KEY_DEVICE_PRODUCT_ID;
static char * const PW_KEY_DEVICE_PRODUCT_NAME;
static char * const PW_KEY_DEVICE_CLASS;
static char * const PW_KEY_DEVICE_FORM_FACTOR;
static char * const PW_KEY_DEVICE_BUS;
static char * const PW_KEY_DEVICE_SUBSYSTEM;
static char * const PW_KEY_DEVICE_ICON;
static char * const PW_KEY_DEVICE_ICON_NAME;
static char * const PW_KEY_DEVICE_INTENDED_ROLES;
static char * const PW_KEY_DEVICE_CACHE_PARAMS;
static char * const PW_KEY_MODULE_ID;
static char * const PW_KEY_MODULE_NAME;
static char * const PW_KEY_MODULE_AUTHOR;
static char * const PW_KEY_MODULE_DESCRIPTION;
static char * const PW_KEY_MODULE_USAGE;
static char * const PW_KEY_MODULE_VERSION;
static char * const PW_KEY_FACTORY_ID;
static char * const PW_KEY_FACTORY_NAME;
static char * const PW_KEY_FACTORY_USAGE;
static char * const PW_KEY_FACTORY_TYPE_NAME;
static char * const PW_KEY_FACTORY_TYPE_VERSION;
static char * const PW_KEY_STREAM_IS_LIVE;
static char * const PW_KEY_STREAM_LATENCY_MIN;
static char * const PW_KEY_STREAM_LATENCY_MAX;
static char * const PW_KEY_STREAM_MONITOR;
static char * const PW_KEY_STREAM_DONT_REMIX;
static char * const PW_KEY_STREAM_CAPTURE_SINK;
static char * const PW_KEY_MEDIA_TYPE;
static char * const PW_KEY_MEDIA_CATEGORY;
static char * const PW_KEY_MEDIA_ROLE;
static char * const PW_KEY_MEDIA_CLASS;
static char * const PW_KEY_MEDIA_NAME;
static char * const PW_KEY_MEDIA_TITLE;
static char * const PW_KEY_MEDIA_ARTIST;
static char * const PW_KEY_MEDIA_COPYRIGHT;
static char * const PW_KEY_MEDIA_SOFTWARE;
static char * const PW_KEY_MEDIA_LANGUAGE;
static char * const PW_KEY_MEDIA_FILENAME;
static char * const PW_KEY_MEDIA_ICON;
static char * const PW_KEY_MEDIA_ICON_NAME;
static char * const PW_KEY_MEDIA_COMMENT;
static char * const PW_KEY_MEDIA_DATE;
static char * const PW_KEY_MEDIA_FORMAT;
static char * const PW_KEY_FORMAT_DSP;
static char * const PW_KEY_AUDIO_CHANNEL;
static char * const PW_KEY_AUDIO_RATE;
static char * const PW_KEY_AUDIO_CHANNELS;
static char * const PW_KEY_AUDIO_FORMAT;
static char * const PW_KEY_VIDEO_RATE;
static char * const PW_KEY_VIDEO_FORMAT;
static char * const PW_KEY_VIDEO_SIZE;
"""

# link.h
CDEF += """
enum pw_link_state {
    PW_LINK_STATE_ERROR,
    PW_LINK_STATE_UNLINKED,
    PW_LINK_STATE_INIT,
    PW_LINK_STATE_NEGOTIATING,
    PW_LINK_STATE_ALLOCATING,
    PW_LINK_STATE_PAUSED,
    PW_LINK_STATE_ACTIVE,
};
struct pw_link_info {
    uint32_t id;
    uint32_t output_node_id;
    uint32_t output_port_id;
    uint32_t input_node_id;
    uint32_t input_port_id;
    uint64_t change_mask;
    enum pw_link_state state;
    const char *error;
    struct spa_pod *format;
    struct spa_dict *props;
};
struct pw_link_events {
    uint32_t version;
    void (*info) (void *object, const struct pw_link_info *info);
};
struct pw_link_methods {
    uint32_t version;
    int (*add_listener) (void *object, struct spa_hook *listener, const struct pw_link_events *events, void *data);
};

static char * const PW_TYPE_INTERFACE_Link;
static const int PW_VERSION_LINK;
static const int PW_LINK_CHANGE_MASK_STATE;
static const int PW_LINK_CHANGE_MASK_FORMAT;
static const int PW_LINK_CHANGE_MASK_PROPS;
static const int PW_LINK_CHANGE_MASK_ALL;
static const int PW_LINK_EVENT_INFO;
static const int PW_LINK_EVENT_NUM;
static const int PW_VERSION_LINK_EVENTS;
static const int PW_LINK_METHOD_ADD_LISTENER;
static const int PW_LINK_METHOD_NUM;
static const int PW_VERSION_LINK_METHODS;
int pw_link_add_listener(struct pw_link *c, struct spa_hook *listener, const struct pw_link_events *events, void *data);

const char *pw_link_state_as_string(enum pw_link_state state);
struct pw_link_info *pw_link_info_update(struct pw_link_info *info, const struct pw_link_info *update);
void pw_link_info_free(struct pw_link_info *info);

extern "Python" {
    void py_cb_pw_link_event_info(void *data, const struct pw_link_info *info);
}
"""

# XXX: macros
# XXX: SPA_PRINTF_FUNC
# NOTE: pw_log_logv not implemented, va_list argument.
# log.h
CDEF += """
extern enum spa_log_level pw_log_level;

void pw_log_set(struct spa_log *log);
struct spa_log *pw_log_get(void);
void pw_log_set_level(enum spa_log_level level);
void pw_log_log(enum spa_log_level level, const char *file, int line, const char *func, const char *fmt, ...);
"""

# XXX: macros
# loop.h
CDEF += """
struct pw_loop {
    struct spa_system *system;
    struct spa_loop *loop;
    struct spa_loop_control *control;
    struct spa_loop_utils *utils;
};

struct pw_loop *pw_loop_new(const struct spa_dict *props);
void pw_loop_destroy(struct pw_loop *loop);
"""

# main-loop.h
CDEF += """
struct pw_main_loop_events {
    uint32_t version;
    void (*destroy) (void *data);
};

static const int PW_VERSION_MAIN_LOOP_EVENTS;

struct pw_main_loop *pw_main_loop_new(const struct spa_dict *props);
void pw_main_loop_add_listener(struct pw_main_loop *loop, struct spa_hook *listener, const struct pw_main_loop_events *events, void *data);
struct pw_loop *pw_main_loop_get_loop(struct pw_main_loop *loop);
void pw_main_loop_destroy(struct pw_main_loop *loop);
int pw_main_loop_run(struct pw_main_loop *loop);
int pw_main_loop_quit(struct pw_main_loop *loop);

extern "Python" {
    void py_cb_pw_main_loop_event_destroy(void *data);
}
"""

# XXX: macros
# map.h
CDEF += """
union pw_map_item {
    uint32_t next;
    void *data;
};
struct pw_map {
    struct pw_array items;
    uint32_t free_list;
};

void pw_map_init(struct pw_map *map, size_t size, size_t extend);
void pw_map_clear(struct pw_map *map);
void pw_map_reset(struct pw_map *map);
uint32_t pw_map_insert_new(struct pw_map *map, void *data);
int pw_map_insert_at(struct pw_map *map, uint32_t id, void *data);
void pw_map_remove(struct pw_map *map, uint32_t id);
void *pw_map_lookup(struct pw_map *map, uint32_t id);
int pw_map_for_each(struct pw_map *map, int (*func) (void *item_data, void *data), void *data);
"""

# NOTE: for some reason, some functions are not exported:
#       struct pw_mempool *pw_mempool_new(struct pw_properties *props);
#       void pw_mempool_add_listener(struct pw_mempool *pool, struct spa_hook *listener, const struct pw_mempool_events *events, void *data);
#       void pw_mempool_clear(struct pw_mempool *pool);
#       void pw_memblock_unref(struct pw_memblock *mem);
#       int pw_mempool_remove_id(struct pw_mempool *pool, uint32_t id);
#       void pw_map_range_init(struct pw_map_range *range, uint32_t offset, uint32_t size, uint32_t page_size);
# XXX: PW_MAP_RANGE_INIT
# mem.h
CDEF += """
enum pw_memblock_flags {
    PW_MEMBLOCK_FLAG_NONE,
    PW_MEMBLOCK_FLAG_READABLE,
    PW_MEMBLOCK_FLAG_WRITABLE,
    PW_MEMBLOCK_FLAG_SEAL,
    PW_MEMBLOCK_FLAG_MAP,
    PW_MEMBLOCK_FLAG_DONT_CLOSE,
    PW_MEMBLOCK_FLAG_DONT_NOTIFY,
    PW_MEMBLOCK_FLAG_READWRITE,
};
enum pw_memmap_flags {
    PW_MEMMAP_FLAG_NONE,
    PW_MEMMAP_FLAG_READ,
    PW_MEMMAP_FLAG_WRITE,
    PW_MEMMAP_FLAG_TWICE,
    PW_MEMMAP_FLAG_PRIVATE,
    PW_MEMMAP_FLAG_LOCKED,
    PW_MEMMAP_FLAG_READWRITE,
};
struct pw_mempool {
    struct pw_properties *props;
};
struct pw_memblock {
    struct pw_mempool *pool;
    uint32_t id;
    int ref;
    uint32_t flags;
    uint32_t type;
    int fd;
    uint32_t size;
    struct pw_memmap *map;
};
struct pw_memmap {
    struct pw_memblock *block;
    void *ptr;
    uint32_t flags;
    uint32_t offset;
    uint32_t size;
    uint32_t tag[5];
};
struct pw_mempool_events {
    uint32_t version;
    void (*destroy) (void *data);
    void (*added) (void *data, struct pw_memblock *block);
    void (*removed) (void *data, struct pw_memblock *block);
};
struct pw_map_range {
    uint32_t start;
    uint32_t offset;
    uint32_t size;
};

static const int PW_VERSION_MEMPOOL_EVENTS;

struct pw_memblock *pw_mempool_alloc(struct pw_mempool *pool, enum pw_memblock_flags flags, uint32_t type, size_t size);
struct pw_memblock *pw_mempool_import_block(struct pw_mempool *pool, struct pw_memblock *mem);
struct pw_memblock *pw_mempool_import(struct pw_mempool *pool, enum pw_memblock_flags flags, uint32_t type, int fd);
void pw_memblock_free(struct pw_memblock *mem);
struct pw_memblock *pw_mempool_find_ptr(struct pw_mempool *pool, const void *ptr);
struct pw_memblock *pw_mempool_find_id(struct pw_mempool *pool, uint32_t id);
struct pw_memblock *pw_mempool_find_fd(struct pw_mempool *pool, int fd);
struct pw_memmap *pw_memblock_map(struct pw_memblock *block, enum pw_memmap_flags flags, uint32_t offset, uint32_t size, uint32_t tag[5]);
struct pw_memmap *pw_mempool_map_id(struct pw_mempool *pool, uint32_t id, enum pw_memmap_flags flags, uint32_t offset, uint32_t size, uint32_t tag[5]);
struct pw_memmap *pw_mempool_import_map(struct pw_mempool *pool, struct pw_mempool *other, void *data, uint32_t size, uint32_t tag[5]);
struct pw_memmap *pw_mempool_find_tag(struct pw_mempool *pool, uint32_t tag[5], size_t size);
int pw_memmap_free(struct pw_memmap *map);

extern "Python" {
    void py_cb_pw_mempool_event_destroy(void *data);
    void py_cb_pw_mempool_event_added(void *data, struct pw_memblock *block);
    void py_cb_pw_mempool_event_removed(void *data, struct pw_memblock *block);
}
"""

# module.h
CDEF += """
struct pw_module_info {
    uint32_t id;
    const char *name;
    const char *filename;
    const char *args;
    uint64_t change_mask;
    struct spa_dict *props;
};
struct pw_module_events {
    uint32_t version;
    void (*info) (void *object, const struct pw_module_info *info);
};
struct pw_module_methods {
    uint32_t version;
    int (*add_listener) (void *object, struct spa_hook *listener, const struct pw_module_events *events, void *data);
};

static char * const PW_TYPE_INTERFACE_Module;
static const int PW_VERSION_MODULE;
static const int PW_MODULE_CHANGE_MASK_PROPS;
static const int PW_MODULE_CHANGE_MASK_ALL;
static const int PW_MODULE_EVENT_INFO;
static const int PW_MODULE_EVENT_NUM;
static const int PW_VERSION_MODULE_EVENTS;
static const int PW_MODULE_METHOD_ADD_LISTENER;
static const int PW_MODULE_METHOD_NUM;
static const int PW_VERSION_MODULE_METHODS;
int pw_module_add_listener(struct pw_module *c, struct spa_hook *listener, const struct pw_module_events *events, void *data);

struct pw_module_info *pw_module_info_update(struct pw_module_info *info, const struct pw_module_info *update);
void pw_module_info_free(struct pw_module_info *info);

extern "Python" {
    void py_cb_pw_module_event_info(void *data, const struct pw_module_info *info);
}
"""

# node.h
CDEF += """
enum pw_node_state {
    PW_NODE_STATE_ERROR,
    PW_NODE_STATE_CREATING,
    PW_NODE_STATE_SUSPENDED,
    PW_NODE_STATE_IDLE,
    PW_NODE_STATE_RUNNING,
};
struct pw_node_info {
    uint32_t id;
    uint32_t max_input_ports;
    uint32_t max_output_ports;
    uint64_t change_mask;
    uint32_t n_input_ports;
    uint32_t n_output_ports;
    enum pw_node_state state;
    const char *error;
    struct spa_dict *props;
    struct spa_param_info *params;
    uint32_t n_params;
};
struct pw_node_events {
    uint32_t version;
    void (*info) (void *object, const struct pw_node_info *info);
    void (*param) (void *object, int seq, uint32_t id, uint32_t index, uint32_t next, const struct spa_pod *param);
};
struct pw_node_methods {
    uint32_t version;
    int (*add_listener) (void *object, struct spa_hook *listener, const struct pw_node_events *events, void *data);
    int (*subscribe_params) (void *object, uint32_t *ids, uint32_t n_ids);
    int (*enum_params) (void *object, int seq, uint32_t id, uint32_t start, uint32_t num, const struct spa_pod *filter);
    int (*set_param) (void *object, uint32_t id, uint32_t flags, const struct spa_pod *param);
    int (*send_command) (void *object, const struct spa_command *command);
};

static char * const PW_TYPE_INTERFACE_Node;
static const int PW_VERSION_NODE;
static const int PW_NODE_CHANGE_MASK_INPUT_PORTS;
static const int PW_NODE_CHANGE_MASK_OUTPUT_PORTS;
static const int PW_NODE_CHANGE_MASK_STATE;
static const int PW_NODE_CHANGE_MASK_PROPS;
static const int PW_NODE_CHANGE_MASK_PARAMS;
static const int PW_NODE_CHANGE_MASK_ALL;
static const int PW_NODE_EVENT_INFO;
static const int PW_NODE_EVENT_PARAM;
static const int PW_NODE_EVENT_NUM;
static const int PW_VERSION_NODE_EVENTS;
static const int PW_NODE_METHOD_ADD_LISTENER;
static const int PW_NODE_METHOD_SUBSCRIBE_PARAMS;
static const int PW_NODE_METHOD_ENUM_PARAMS;
static const int PW_NODE_METHOD_SET_PARAM;
static const int PW_NODE_METHOD_SEND_COMMAND;
static const int PW_NODE_METHOD_NUM;
static const int PW_VERSION_NODE_METHODS;
int pw_node_add_listener(struct pw_node *c, struct spa_hook *listener, const struct pw_node_events *events, void *data);
int pw_node_subscribe_params(struct pw_node *c, uint32_t *ids, uint32_t n_ids);
int pw_node_enum_params(struct pw_node *c, int seq, uint32_t id, uint32_t start, uint32_t num, const struct spa_pod *filter);
int pw_node_set_param(struct pw_node *c, uint32_t id, uint32_t flags, const struct spa_pod *param);
int pw_node_send_command(struct pw_node *c, const struct spa_command *command);

const char *pw_node_state_as_string(enum pw_node_state state);
struct pw_node_info *pw_node_info_update(struct pw_node_info *info, const struct pw_node_info *update);
void pw_node_info_free(struct pw_node_info *info);

extern "Python" {
    void py_cb_pw_node_event_info(void *data, const struct pw_node_info *info);
    void py_cb_pw_node_event_param(void *data, int seq, uint32_t id, uint32_t index, uint32_t next, const struct spa_pod *param);
}
"""

# XXX: PW_PERMISSION_INIT(id, p), PW_PERMISSION_ARGS(permission)
# permission.h
CDEF += """
struct pw_permission {
    uint32_t id;
    uint32_t permissions;
};

static const int PW_PERM_R;
static const int PW_PERM_W;
static const int PW_PERM_X;
static const int PW_PERM_M;
static const int PW_PERM_RWX;
static const int PW_PERM_RWXM;
static const int PW_PERM_ALL;
static const uint32_t PW_PERM_INVALID;
bool PW_PERM_IS_R(uint32_t p);
bool PW_PERM_IS_W(uint32_t p);
bool PW_PERM_IS_X(uint32_t p);
bool PW_PERM_IS_M(uint32_t p);
"""

# pipewire.h
CDEF += """
void pw_init(int *argc, char **argv[]);
void pw_deinit(void);
bool pw_debug_is_category_enabled(const char *name);
const char *pw_get_application_name(void);
const char *pw_get_prgname(void);
const char *pw_get_user_name(void);
const char *pw_get_host_name(void);
const char *pw_get_client_name(void);
bool pw_in_valgrind(void);
enum pw_direction pw_direction_reverse(enum pw_direction direction);
int pw_set_domain(const char *domain);
const char *pw_get_domain(void);
uint32_t pw_get_support(struct spa_support *support, uint32_t max_support);
struct spa_handle *pw_load_spa_handle(const char *lib, const char *factory_name, const struct spa_dict *info, uint32_t n_support, const struct spa_support support[]);
int pw_unload_spa_handle(struct spa_handle *handle);
"""

# port.h
CDEF += """
struct pw_port_info {
    uint32_t id;
    enum pw_direction direction;
    uint64_t change_mask;
    struct spa_dict *props;
    struct spa_param_info *params;
    uint32_t n_params;
};
struct pw_port_events {
    uint32_t version;
    void (*info) (void *object, const struct pw_port_info *info);
    void (*param) (void *object, int seq, uint32_t id, uint32_t index, uint32_t next, const struct spa_pod *param);
};
struct pw_port_methods {
    uint32_t version;
    int (*add_listener) (void *object, struct spa_hook *listener, const struct pw_port_events *events, void *data);
    int (*subscribe_params) (void *object, uint32_t *ids, uint32_t n_ids);
    int (*enum_params) (void *object, int seq, uint32_t id, uint32_t start, uint32_t num, const struct spa_pod *filter);
};

static char * const PW_TYPE_INTERFACE_Port;
static const int PW_VERSION_PORT;
static const int PW_PORT_CHANGE_MASK_PROPS;
static const int PW_PORT_CHANGE_MASK_PARAMS;
static const int PW_PORT_CHANGE_MASK_ALL;
static const int PW_PORT_EVENT_INFO;
static const int PW_PORT_EVENT_PARAM;
static const int PW_PORT_EVENT_NUM;
static const int PW_VERSION_PORT_EVENTS;
static const int PW_PORT_METHOD_ADD_LISTENER;
static const int PW_PORT_METHOD_SUBSCRIBE_PARAMS;
static const int PW_PORT_METHOD_ENUM_PARAMS;
static const int PW_PORT_METHOD_NUM;
static const int PW_VERSION_PORT_METHODS;
int pw_port_add_listener(struct pw_port *c, struct spa_hook *listener, const struct pw_port_events *events, void *data);
int pw_port_subscribe_params(struct pw_port *c, uint32_t *ids, uint32_t n_ids);
int pw_port_enum_params(struct pw_port *c, int seq, uint32_t id, uint32_t start, uint32_t num, const struct spa_pod *filter);

const char *pw_direction_as_string(enum pw_direction direction);
struct pw_port_info *pw_port_info_update(struct pw_port_info *info, const struct pw_port_info *update);
void pw_port_info_free(struct pw_port_info *info);

extern "Python" {
    void py_cb_pw_port_event_info(void *data, const struct pw_port_info *info);
    void py_cb_pw_port_event_param(void *data, int seq, uint32_t id, uint32_t index, uint32_t next, const struct spa_pod *param);
}
"""

# XXX: SPA_SENTINEL
# XXX: SPA_PRINTF_FUNC
# NOTE: pw_properties_setva not implemented, va_list argument.
# properties.h
CDEF += """
struct pw_properties {
    struct spa_dict dict;
    uint32_t flags;
};

static const int PW_PROPERTIES_FLAG_NL;

struct pw_properties *pw_properties_new(const char *key, ...);
struct pw_properties *pw_properties_new_dict(const struct spa_dict *dict);
struct pw_properties *pw_properties_new_string(const char *args);
struct pw_properties *pw_properties_copy(const struct pw_properties *properties);
int pw_properties_update_keys(struct pw_properties *props, const struct spa_dict *dict, const char * const keys[]);
int pw_properties_update_ignore(struct pw_properties *props, const struct spa_dict *dict, const char * const ignore[]);
int pw_properties_update(struct pw_properties *props, const struct spa_dict *dict);
int pw_properties_update_string(struct pw_properties *props, const char *str, size_t size);
int pw_properties_add(struct pw_properties *oldprops, const struct spa_dict *dict);
int pw_properties_add_keys(struct pw_properties *oldprops, const struct spa_dict *dict, const char * const keys[]);
void pw_properties_clear(struct pw_properties *properties);
void pw_properties_free(struct pw_properties *properties);
int pw_properties_set(struct pw_properties *properties, const char *key, const char *value);
int pw_properties_setf(struct pw_properties *properties, const char *key, const char *format, ...);
const char *pw_properties_get(const struct pw_properties *properties, const char *key);
const char *pw_properties_iterate(const struct pw_properties *properties, void **state);
int pw_properties_serialize_dict(FILE *f, const struct spa_dict *dict, uint32_t flags);
bool pw_properties_parse_bool(const char *value);
int pw_properties_parse_int(const char *value);
int64_t pw_properties_parse_int64(const char *value);
uint64_t pw_properties_parse_uint64(const char *value);
float pw_properties_parse_float(const char *value);
double pw_properties_parse_double(const char *value);
"""

# XXX: macros
# protocol.h
CDEF += """
struct pw_protocol_client {
    struct spa_list link;
    struct pw_protocol *protocol;
    struct pw_core *core;
    int (*connect) (struct pw_protocol_client *client, const struct spa_dict *props, void (*done_callback) (void *data, int result), void *data);
    int (*connect_fd) (struct pw_protocol_client *client, int fd, bool close);
    int (*steal_fd) (struct pw_protocol_client *client);
    void (*disconnect) (struct pw_protocol_client *client);
    void (*destroy) (struct pw_protocol_client *client);
    int (*set_paused) (struct pw_protocol_client *client, bool paused);
};
struct pw_protocol_server {
    struct spa_list link;
    struct pw_protocol *protocol;
    struct pw_impl_core *core;
    struct spa_list client_list;
    void (*destroy) (struct pw_protocol_server *listen);
};
struct pw_protocol_marshal {
    const char *type;
    uint32_t version;
    uint32_t flags;
    uint32_t n_client_methods;
    uint32_t n_server_methods;
    const void *client_marshal;
    const void *server_demarshal;
    const void *server_marshal;
    const void *client_demarshal;
};
struct pw_protocol_implementation {
    uint32_t version;
    struct pw_protocol_client * (*new_client) (struct pw_protocol *protocol, struct pw_core *core, const struct spa_dict *props);
    struct pw_protocol_server * (*add_server) (struct pw_protocol *protocol, struct pw_impl_core *core, const struct spa_dict *props);
};
struct pw_protocol_events {
    uint32_t version;
    void (*destroy) (void *data);
};

static char * const PW_TYPE_INFO_Protocol;
static char * const PW_TYPE_INFO_PROTOCOL_BASE;
static const int PW_VERSION_PROTOCOL_EVENTS;

struct pw_protocol *pw_protocol_new(struct pw_context *context, const char *name, size_t user_data_size);
void pw_protocol_destroy(struct pw_protocol *protocol);
struct pw_context *pw_protocol_get_context(struct pw_protocol *protocol);
void *pw_protocol_get_user_data(struct pw_protocol *protocol);
const struct pw_protocol_implementation *pw_protocol_get_implementation(struct pw_protocol *protocol);
const void *pw_protocol_get_extension(struct pw_protocol *protocol);
void pw_protocol_add_listener(struct pw_protocol *protocol, struct spa_hook *listener, const struct pw_protocol_events *events, void *data);
int pw_protocol_add_marshal(struct pw_protocol *protocol, const struct pw_protocol_marshal *marshal);
const struct pw_protocol_marshal *pw_protocol_get_marshal(struct pw_protocol *protocol, const char *type, uint32_t version, uint32_t flags);
struct pw_protocol *pw_context_find_protocol(struct pw_context *context, const char *name);

extern "Python" {
    void py_cb_pw_protocol_event_destroy(void *data);
}
"""

# XXX: SPA_PRINTF_FUNC
# XXX: how to declare pw_proxy_(notify|call(_res))???
# proxy.h
CDEF += """
struct pw_proxy_events {
    uint32_t version;
    void (*destroy) (void *data);
    void (*bound) (void *data, uint32_t global_id);
    void (*removed) (void *data);
    void (*done) (void *data, int seq);
    void (*error) (void *data, int seq, int res, const char *message);
};

static const int PW_VERSION_PROXY_EVENTS;

struct pw_proxy *pw_proxy_new(struct pw_proxy *factory, const char *type, uint32_t version, size_t user_data_size);
void pw_proxy_add_listener(struct pw_proxy *proxy, struct spa_hook *listener, const struct pw_proxy_events *events, void *data);
void pw_proxy_add_object_listener(struct pw_proxy *proxy, struct spa_hook *listener, const void *funcs, void *data);
void pw_proxy_destroy(struct pw_proxy *proxy);
void *pw_proxy_get_user_data(struct pw_proxy *proxy);
uint32_t pw_proxy_get_id(struct pw_proxy *proxy);
const char *pw_proxy_get_type(struct pw_proxy *proxy, uint32_t *version);
struct pw_protocol *pw_proxy_get_protocol(struct pw_proxy *proxy);
int pw_proxy_sync(struct pw_proxy *proxy, int seq);
int pw_proxy_set_bound_id(struct pw_proxy *proxy, uint32_t global_id);
uint32_t pw_proxy_get_bound_id(struct pw_proxy *proxy);
int pw_proxy_error(struct pw_proxy *proxy, int res, const char *error);
int pw_proxy_errorf(struct pw_proxy *proxy, int res, const char *error, ...);
struct spa_hook_list *pw_proxy_get_object_listeners(struct pw_proxy *proxy);
const struct pw_protocol_marshal *pw_proxy_get_marshal(struct pw_proxy *proxy);
int pw_proxy_install_marshal(struct pw_proxy *proxy, bool implementor);

extern "Python" {
    void py_cb_pw_proxy_event_destroy(void *data);
    void py_cb_pw_proxy_event_bound(void *data, uint32_t global_id);
    void py_cb_pw_proxy_event_removed(void *data);
    void py_cb_pw_proxy_event_done(void *data, int seq);
    void py_cb_pw_proxy_event_error(void *data, int seq, int res, const char *message);
}
"""

# XXX: SPA_PRINTF_FUNC
# XXX: >0.3.34 const struct pw_stream_control *pw_stream_get_control(struct pw_stream *stream, uint32_t id);
#              fc9f7c1005e5ab06c6ef7628169b4b59a3b83c48
# stream.h
CDEF += """
enum pw_stream_state {
    PW_STREAM_STATE_ERROR,
    PW_STREAM_STATE_UNCONNECTED,
    PW_STREAM_STATE_CONNECTING,
    PW_STREAM_STATE_PAUSED,
    PW_STREAM_STATE_STREAMING,
};
struct pw_buffer {
    struct spa_buffer *buffer;
    void *user_data;
    uint64_t size;
};
struct pw_stream_control {
    const char *name;
    uint32_t flags;
    float def;
    float min;
    float max;
    float *values;
    uint32_t n_values;
    uint32_t max_values;
};
struct pw_time {
    int64_t now;
    struct spa_fraction rate;
    uint64_t ticks;
    int64_t delay;
    uint64_t queued;
};
struct pw_stream_events {
    uint32_t version;
    void (*destroy) (void *data);
    void (*state_changed) (void *data, enum pw_stream_state old, enum pw_stream_state state, const char *error);
    void (*control_info) (void *data, uint32_t id, const struct pw_stream_control *control);
    void (*io_changed) (void *data, uint32_t id, void *area, uint32_t size);
    void (*param_changed) (void *data, uint32_t id, const struct spa_pod *param);
    void (*add_buffer) (void *data, struct pw_buffer *buffer);
    void (*remove_buffer) (void *data, struct pw_buffer *buffer);
    void (*process) (void *data);
    void (*drained) (void *data);
};
enum pw_stream_flags {
    PW_STREAM_FLAG_NONE,
    PW_STREAM_FLAG_AUTOCONNECT,
    PW_STREAM_FLAG_INACTIVE,
    PW_STREAM_FLAG_MAP_BUFFERS,
    PW_STREAM_FLAG_DRIVER,
    PW_STREAM_FLAG_RT_PROCESS,
    PW_STREAM_FLAG_NO_CONVERT,
    PW_STREAM_FLAG_EXCLUSIVE,
    PW_STREAM_FLAG_DONT_RECONNECT,
    PW_STREAM_FLAG_ALLOC_BUFFERS,
};

static const int PW_VERSION_STREAM_EVENTS;

const char *pw_stream_state_as_string(enum pw_stream_state state);
struct pw_stream *pw_stream_new(struct pw_core *core, const char *name, struct pw_properties *props);
struct pw_stream *pw_stream_new_simple(struct pw_loop *loop, const char *name, struct pw_properties *props, const struct pw_stream_events *events, void *data);
void pw_stream_destroy(struct pw_stream *stream);
void pw_stream_add_listener(struct pw_stream *stream, struct spa_hook *listener, const struct pw_stream_events *events, void *data);
enum pw_stream_state pw_stream_get_state(struct pw_stream *stream, const char **error);
const char *pw_stream_get_name(struct pw_stream *stream);
struct pw_core *pw_stream_get_core(struct pw_stream *stream);
const struct pw_properties *pw_stream_get_properties(struct pw_stream *stream);
int pw_stream_update_properties(struct pw_stream *stream, const struct spa_dict *dict);
int pw_stream_connect(struct pw_stream *stream, enum pw_direction direction, uint32_t target_id, enum pw_stream_flags flags, const struct spa_pod **params, uint32_t n_params);
uint32_t pw_stream_get_node_id(struct pw_stream *stream);
int pw_stream_disconnect(struct pw_stream *stream);
int pw_stream_set_error(struct pw_stream *stream, int res, const char *error, ...);
int pw_stream_update_params(struct pw_stream *stream, const struct spa_pod **params, uint32_t n_params);
int pw_stream_set_control(struct pw_stream *stream, uint32_t id, uint32_t n_values, float *values, ...);
int pw_stream_get_time(struct pw_stream *stream, struct pw_time *time);
struct pw_buffer *pw_stream_dequeue_buffer(struct pw_stream *stream);
int pw_stream_queue_buffer(struct pw_stream *stream, struct pw_buffer *buffer);
int pw_stream_set_active(struct pw_stream *stream, bool active);
int pw_stream_flush(struct pw_stream *stream, bool drain);
bool pw_stream_is_driving(struct pw_stream *stream);
int pw_stream_trigger_process(struct pw_stream *stream);

extern "Python" {
    void py_cb_pw_stream_event_destroy(void *data);
    void py_cb_pw_stream_event_state_changed(void *data, enum pw_stream_state old, enum pw_stream_state state, const char *error);
    void py_cb_pw_stream_event_control_info(void *data, uint32_t id, const struct pw_stream_control *control);
    void py_cb_pw_stream_event_io_changed(void *data, uint32_t id, void *area, uint32_t size);
    void py_cb_pw_stream_event_param_changed(void *data, uint32_t id, const struct spa_pod *param);
    void py_cb_pw_stream_event_add_buffer(void *data, struct pw_buffer *buffer);
    void py_cb_pw_stream_event_remove_buffer(void *data, struct pw_buffer *buffer);
    void py_cb_pw_stream_event_process(void *data);
    void py_cb_pw_stream_event_drained(void *data);
}
"""

# thread-loop.h
CDEF += """
struct pw_thread_loop_events {
    uint32_t version;
    void (*destroy) (void *data);
};

static const int PW_VERSION_THREAD_LOOP_EVENTS;

struct pw_thread_loop *pw_thread_loop_new(const char *name, const struct spa_dict *props);
struct pw_thread_loop *pw_thread_loop_new_full(struct pw_loop *loop, const char *name, const struct spa_dict *props);
void pw_thread_loop_destroy(struct pw_thread_loop *loop);
void pw_thread_loop_add_listener(struct pw_thread_loop *loop, struct spa_hook *listener, const struct pw_thread_loop_events *events, void *data);
struct pw_loop *pw_thread_loop_get_loop(struct pw_thread_loop *loop);
int pw_thread_loop_start(struct pw_thread_loop *loop);
void pw_thread_loop_stop(struct pw_thread_loop *loop);
void pw_thread_loop_lock(struct pw_thread_loop *loop);
void pw_thread_loop_unlock(struct pw_thread_loop *loop);
void pw_thread_loop_wait(struct pw_thread_loop *loop);
int pw_thread_loop_timed_wait(struct pw_thread_loop *loop, int wait_max_sec);
int pw_thread_loop_get_time(struct pw_thread_loop *loop, struct timespec *abstime, int64_t timeout);
int pw_thread_loop_timed_wait_full(struct pw_thread_loop *loop, struct timespec *abstime);
void pw_thread_loop_signal(struct pw_thread_loop *loop, bool wait_for_accept);
void pw_thread_loop_accept(struct pw_thread_loop *loop);
bool pw_thread_loop_in_thread(struct pw_thread_loop *loop);

extern "Python" {
    void py_cb_pw_thread_loop_event_destroy(void *data);
}
"""

# type.h
CDEF += """
enum {
    PW_TYPE_FIRST,
};

static char * const PW_TYPE_INFO_BASE;
static char * const PW_TYPE_INFO_Object;
static char * const PW_TYPE_INFO_OBJECT_BASE;
static char * const PW_TYPE_INFO_Interface;
static char * const PW_TYPE_INFO_INTERFACE_BASE;

const struct spa_type_info *pw_type_info(void);
"""

# XXX: should we really expose str(n)dupa?
# utils.h
CDEF += """
typedef ... pw_destroy_t;
const char *pw_split_walk(const char *str, const char *delimiter, size_t *len, const char **state);
char **pw_split_strv(const char *str, const char *delimiter, int max_tokens, int *n_tokens);
void pw_free_strv(char **str);
char *pw_strip(char *str, const char *whitespace);
char *strndupa(const char *s, int n);
char *strdupa(const char *s);
"""

# XXX: pw_get_headers_version()
# version.h.in
CDEF += """
static char * const PW_API_VERSION;
static const int PW_MAJOR;
static const int PW_MINOR;
static const int PW_MICRO;
bool PW_CHECK_VERSION(int major, int minor, int micro);

const char* pw_get_library_version(void);
"""



ffi_builder = FFI()
ffi_builder.include(build_spa.ffi_builder)
# XXX: cffi requires that *all* elements included via ffi_builder.include(...) are actually reached in the includer's source... ugly way, just include the whole list of SPA headers...
#      see also https://foss.heptapod.net/pypy/cffi/-/issues/420
SOURCE += build_spa.SOURCE
ffi_builder.cdef(CDEF)
ffi_builder.set_source_pkgconfig(
    "pipewire._ffi_pipewire",
    # XXX: dynamic version?
    ["libpipewire-0.3"],
    SOURCE,
)


def build():
    ffi_builder.compile()


if __name__ == "__main__":
    build_spa.build()
    build()
