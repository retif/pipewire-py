from cffi import FFI


SOURCE = ""

CDEF = ""

# forwards
# enums/structs/types
# macros
# fcts
# vars
# py fcts

SOURCE += """
#include <spa/buffer/alloc.h>
"""
CDEF += """
struct spa_buffer_alloc_info {
    uint32_t flags;
    uint32_t max_align;
    uint32_t n_metas;
    uint32_t n_datas;
    struct spa_meta *metas;
    struct spa_data *datas;
    uint32_t *data_aligns;
    size_t skel_size;
    size_t meta_size;
    size_t chunk_size;
    size_t data_size;
    size_t mem_size;
};

static const int SPA_BUFFER_ALLOC_FLAG_INLINE_META;
static const int SPA_BUFFER_ALLOC_FLAG_INLINE_CHUNK;
static const int SPA_BUFFER_ALLOC_FLAG_INLINE_DATA;
static const int SPA_BUFFER_ALLOC_FLAG_INLINE_ALL;
static const int SPA_BUFFER_ALLOC_FLAG_NO_DATA;

int spa_buffer_alloc_fill_info(struct spa_buffer_alloc_info *info, uint32_t n_metas, struct spa_meta metas[], uint32_t n_datas, struct spa_data datas[], uint32_t data_aligns[]);
struct spa_buffer *spa_buffer_alloc_layout(struct spa_buffer_alloc_info *info, void *skel_mem, void *data_mem);
int spa_buffer_alloc_layout_array(struct spa_buffer_alloc_info *info, uint32_t n_buffers, struct spa_buffer *buffers[], void *skel_mem, void *data_mem);
struct spa_buffer **spa_buffer_alloc_array(uint32_t n_buffers, uint32_t flags, uint32_t n_metas, struct spa_meta metas[], uint32_t n_datas, struct spa_data datas[], uint32_t data_aligns[]);
"""

SOURCE += """
#include <spa/buffer/buffer.h>
"""
CDEF += """
enum spa_data_type {
    SPA_DATA_Invalid,
    SPA_DATA_MemPtr,
    SPA_DATA_MemFd,
    SPA_DATA_DmaBuf,
    SPA_DATA_MemId,
};
struct spa_chunk {
    uint32_t offset;
    uint32_t size;
    int32_t stride;
    int32_t flags;
};
struct spa_data {
    uint32_t type;
    uint32_t flags;
    int64_t fd;
    uint32_t mapoffset;
    uint32_t maxsize;
    void *data;
    struct spa_chunk *chunk;
};
struct spa_buffer {
    uint32_t n_metas;
    uint32_t n_datas;
    struct spa_meta *metas;
    struct spa_data *datas;
};

static const int SPA_CHUNK_FLAG_NONE;
static const int SPA_CHUNK_FLAG_CORRUPTED;
static const int SPA_DATA_FLAG_NONE;
static const int SPA_DATA_FLAG_READABLE;
static const int SPA_DATA_FLAG_WRITABLE;
static const int SPA_DATA_FLAG_DYNAMIC;
static const int SPA_DATA_FLAG_READWRITE;

struct spa_meta *spa_buffer_find_meta(const struct spa_buffer *b, uint32_t type);
void *spa_buffer_find_meta_data(const struct spa_buffer *b, uint32_t type, size_t size);
"""

# XXX: spa_meta_for_each
# XXX: is spa_meta_check correct??
SOURCE += """
#include <spa/buffer/meta.h>
"""
CDEF += """
enum spa_meta_type {
    SPA_META_Invalid,
    SPA_META_Header,
    SPA_META_VideoCrop,
    SPA_META_VideoDamage,
    SPA_META_Bitmap,
    SPA_META_Cursor,
    SPA_META_Control,
    SPA_META_Busy,
};
struct spa_meta {
    uint32_t type;
    uint32_t size;
    void *data;
};
struct spa_meta_header {
    uint32_t flags;
    uint32_t offset;
    int64_t pts;
    int64_t dts_offset;
    uint64_t seq;
};
struct spa_meta_region {
    struct spa_region region;
};
struct spa_meta_bitmap {
    uint32_t format;
    struct spa_rectangle size;
    int32_t stride;
    uint32_t offset;
};
struct spa_meta_cursor {
    uint32_t id;
    uint32_t flags;
    struct spa_point position;
    struct spa_point hotspot;
    uint32_t bitmap_offset;
};
struct spa_meta_control {
    struct spa_pod_sequence sequence;
};
struct spa_meta_busy {
    uint32_t flags;
    uint32_t count;
};

static const int SPA_META_HEADER_FLAG_DISCONT;
static const int SPA_META_HEADER_FLAG_CORRUPTED;
static const int SPA_META_HEADER_FLAG_MARKER;
static const int SPA_META_HEADER_FLAG_HEADER;
static const int SPA_META_HEADER_FLAG_GAP;
static const int SPA_META_HEADER_FLAG_DELTA_UNIT;
void *spa_meta_first(struct spa_meta *m);
void *spa_meta_end(struct spa_meta *m);
bool spa_meta_check(void *p, struct spa_meta *m);
bool spa_meta_region_is_valid(struct spa_meta_region *m);
bool spa_meta_bitmap_is_valid(struct spa_meta_bitmap *m);
bool spa_meta_cursor_is_valid(struct spa_meta_cursor *m);
"""

SOURCE += """
#include <spa/buffer/type-info.h>
"""
CDEF += """
static char * const SPA_TYPE_INFO_Buffer;
static char * const SPA_TYPE_INFO_BUFFER_BASE;
static char * const SPA_TYPE_INFO_Data;
static char * const SPA_TYPE_INFO_DATA_BASE;
static char * const SPA_TYPE_INFO_DATA_Fd;
static char * const SPA_TYPE_INFO_DATA_FD_BASE;
static char * const SPA_TYPE_INFO_Meta;
static char * const SPA_TYPE_INFO_META_BASE;
static char * const SPA_TYPE_INFO_META_Array;
static char * const SPA_TYPE_INFO_META_ARRAY_BASE;
static char * const SPA_TYPE_INFO_META_Region;
static char * const SPA_TYPE_INFO_META_REGION_BASE;
static char * const SPA_TYPE_INFO_META_ARRAY_Region;
static char * const SPA_TYPE_INFO_META_ARRAY_REGION_BASE;

static const struct spa_type_info spa_type_data_type[...];
static const struct spa_type_info spa_type_meta_type[...];
"""


SOURCE += """
#include <spa/control/control.h>
"""
CDEF += """
enum spa_control_type {
    SPA_CONTROL_Invalid,
    SPA_CONTROL_Properties,
    SPA_CONTROL_Midi,
    SPA_CONTROL_OSC,
};
"""

SOURCE += """
#include <spa/control/type-info.h>
"""
CDEF += """
static char * const SPA_TYPE_INFO_Control;
static char * const SPA_TYPE_INFO_CONTROL_BASE;

static const struct spa_type_info spa_type_control[...];
"""


# XXX: spa_debug(...)
SOURCE += """
#include <spa/debug/buffer.h>
"""
CDEF += """
int spa_debug_buffer(int indent, const struct spa_buffer *buffer);
"""

# XXX: spa_debug(...)
SOURCE += """
#include <spa/debug/dict.h>
"""
CDEF += """
int spa_debug_dict(int indent, const struct spa_dict *dict);
"""

SOURCE += """
#include <spa/debug/format.h>
"""
CDEF += """
int spa_debug_format_value(const struct spa_type_info *info, uint32_t type, void *body, uint32_t size);
int spa_debug_format(int indent, const struct spa_type_info *info, const struct spa_pod *format);
"""

# XXX: spa_debug(...)
SOURCE += """
#include <spa/debug/mem.h>
"""
CDEF += """
int spa_debug_mem(int indent, const void *data, size_t size);
"""

# XXX: spa_debug(...)
SOURCE += """
#include <spa/debug/node.h>
"""
CDEF += """
int spa_debug_port_info(int indent, const struct spa_port_info *info);
"""

# XXX: spa_debug(...)
SOURCE += """
#include <spa/debug/pod.h>
"""
CDEF += """
int spa_debug_pod_value(int indent, const struct spa_type_info *info, uint32_t type, void *body, uint32_t size);
int spa_debug_pod(int indent, const struct spa_type_info *info, const struct spa_pod *pod);
"""

SOURCE += """
#include <spa/debug/types.h>
"""
CDEF += """
const struct spa_type_info *spa_debug_type_find(const struct spa_type_info *info, uint32_t type);
const char *spa_debug_type_short_name(const char *name);
const char *spa_debug_type_find_name(const struct spa_type_info *info, uint32_t type);
const char *spa_debug_type_find_short_name(const struct spa_type_info *info, uint32_t type);
uint32_t spa_debug_type_find_type(const struct spa_type_info *info, const char *name);
"""


# NOTE: enum spa_direction is actually defined in <spa/utils/defs.h>, but needs to be {}-declared on the first mention.
# XXX: spa_debug(...)
SOURCE += """
#include <spa/graph/graph.h>
"""
CDEF += """
enum spa_direction {
    SPA_DIRECTION_INPUT,
    SPA_DIRECTION_OUTPUT,
};

struct spa_graph_state {
    int status;
    int32_t required;
    int32_t pending;
};
struct spa_graph_link {
    struct spa_list link;
    struct spa_graph_state *state;
    int (*signal) (void *data);
    void *signal_data;
};
struct spa_graph {
    uint32_t flags;
    struct spa_graph_node *parent;
    struct spa_graph_state *state;
    struct spa_list nodes;
};
struct spa_graph_node_callbacks {
    uint32_t version;
    int (*process) (void *data, struct spa_graph_node *node);
    int (*reuse_buffer) (void *data, struct spa_graph_node *node, uint32_t port_id, uint32_t buffer_id);
};
struct spa_graph_node {
    struct spa_list link;
    struct spa_graph *graph;
    struct spa_list ports[2];
    struct spa_list links;
    uint32_t flags;
    struct spa_graph_state *state;
    struct spa_graph_link graph_link;
    struct spa_graph *subgraph;
    struct spa_callbacks callbacks;
    struct spa_list sched_link;
};
struct spa_graph_port {
    struct spa_list link;
    struct spa_graph_node *node;
    enum spa_direction direction;
    uint32_t port_id;
    uint32_t flags;
    struct spa_graph_port *peer;
};

static const int SPA_VERSION_GRAPH_NODE_CALLBACKS;
int spa_graph_link_signal(struct spa_graph_link *l);
bool spa_graph_state_dec(struct spa_graph_state *s, int32_t c);
int spa_graph_node_process(struct spa_graph_node *n);
int spa_graph_node_reuse_buffer(struct spa_graph_node *n, uint32_t p, uint32_t i);

void spa_graph_state_reset(struct spa_graph_state *state);
int spa_graph_link_trigger(struct spa_graph_link *link);
int spa_graph_node_trigger(struct spa_graph_node *node);
int spa_graph_run(struct spa_graph *graph);
int spa_graph_finish(struct spa_graph *graph);
int spa_graph_link_signal_node(void *data);
int spa_graph_link_signal_graph(void *data);
void spa_graph_init(struct spa_graph *graph, struct spa_graph_state *state);
void spa_graph_link_add(struct spa_graph_node *out, struct spa_graph_state *state, struct spa_graph_link *link);
void spa_graph_link_remove(struct spa_graph_link *link);
void spa_graph_node_init(struct spa_graph_node *node, struct spa_graph_state *state);
int spa_graph_node_impl_sub_process(void *data, struct spa_graph_node *node);
void spa_graph_node_set_subgraph(struct spa_graph_node *node, struct spa_graph *subgraph);
void spa_graph_node_set_callbacks(struct spa_graph_node *node, const struct spa_graph_node_callbacks *callbacks, void *data);
void spa_graph_node_add(struct spa_graph *graph, struct spa_graph_node *node);
void spa_graph_node_remove(struct spa_graph_node *node);
void spa_graph_port_init(struct spa_graph_port *port, enum spa_direction direction, uint32_t port_id, uint32_t flags);
void spa_graph_port_add(struct spa_graph_node *node, struct spa_graph_port *port);
void spa_graph_port_remove(struct spa_graph_port *port);
void spa_graph_port_link(struct spa_graph_port *out, struct spa_graph_port *in);
void spa_graph_port_unlink(struct spa_graph_port *port);
int spa_graph_node_impl_process(void *data, struct spa_graph_node *node);
int spa_graph_node_impl_reuse_buffer(void *data, struct spa_graph_node *node, uint32_t port_id, uint32_t buffer_id);

static const struct spa_graph_node_callbacks spa_graph_node_sub_impl_default;
static const struct spa_graph_node_callbacks spa_graph_node_impl_default;

extern "Python" {
    int py_cb_spa_graph_node_callback_process(void *data, struct spa_graph_node *node);
    int py_cb_spa_graph_node_callback_reuse_buffer(void *data, struct spa_graph_node *node, uint32_t port_id, uint32_t buffer_id);
}
"""


# XXX: SPA_DEVICE_INFO_INIT(), SPA_DEVICE_OBJECT_INFO_INIT()
SOURCE += """
#include <spa/monitor/device.h>
"""
CDEF += """
struct spa_device {
    struct spa_interface iface;
};
struct spa_device_info {
    uint32_t version;
    uint64_t change_mask;
    uint64_t flags;
    const struct spa_dict *props;
    struct spa_param_info *params;
    uint32_t n_params;
};
struct spa_device_object_info {
    uint32_t version;
    const char *type;
    const char *factory_name;
    uint64_t change_mask;
    uint64_t flags;
    const struct spa_dict *props;
};
struct spa_result_device_params {
    uint32_t id;
    uint32_t index;
    uint32_t next;
    struct spa_pod *param;
};
struct spa_device_events {
    uint32_t version;
    void (*info) (void *data, const struct spa_device_info *info);
    void (*result) (void *data, int seq, int res, uint32_t type, const void *result);
    void (*event) (void *data, const struct spa_event *event);
    void (*object_info) (void *data, uint32_t id, const struct spa_device_object_info *info);
};
struct spa_device_methods {
    uint32_t version;
    int (*add_listener) (void *object, struct spa_hook *listener, const struct spa_device_events *events, void *data);
    int (*sync) (void *object, int seq);
    int (*enum_params) (void *object, int seq, uint32_t id, uint32_t index, uint32_t max, const struct spa_pod *filter);
    int (*set_param) (void *object, uint32_t id, uint32_t flags, const struct spa_pod *param);
};

static char * const SPA_TYPE_INTERFACE_Device;
static const int SPA_VERSION_DEVICE;
static const int SPA_VERSION_DEVICE_INFO;
static const int SPA_DEVICE_CHANGE_MASK_FLAGS;
static const int SPA_DEVICE_CHANGE_MASK_PROPS;
static const int SPA_DEVICE_CHANGE_MASK_PARAMS;
static const int SPA_VERSION_DEVICE_OBJECT_INFO;
static const int SPA_DEVICE_OBJECT_CHANGE_MASK_FLAGS;
static const int SPA_DEVICE_OBJECT_CHANGE_MASK_PROPS;
static const int SPA_RESULT_TYPE_DEVICE_PARAMS;
static const int SPA_DEVICE_EVENT_INFO;
static const int SPA_DEVICE_EVENT_RESULT;
static const int SPA_DEVICE_EVENT_EVENT;
static const int SPA_DEVICE_EVENT_OBJECT_INFO;
static const int SPA_DEVICE_EVENT_NUM;
static const int SPA_VERSION_DEVICE_EVENTS;
static const int SPA_DEVICE_METHOD_ADD_LISTENER;
static const int SPA_DEVICE_METHOD_SYNC;
static const int SPA_DEVICE_METHOD_ENUM_PARAMS;
static const int SPA_DEVICE_METHOD_SET_PARAM;
static const int SPA_DEVICE_METHOD_NUM;
static const int SPA_VERSION_DEVICE_METHODS;
static char * const SPA_KEY_DEVICE_ENUM_API;
static char * const SPA_KEY_DEVICE_API;
static char * const SPA_KEY_DEVICE_NAME;
static char * const SPA_KEY_DEVICE_ALIAS;
static char * const SPA_KEY_DEVICE_NICK;
static char * const SPA_KEY_DEVICE_DESCRIPTION;
static char * const SPA_KEY_DEVICE_ICON;
static char * const SPA_KEY_DEVICE_ICON_NAME;
static char * const SPA_KEY_DEVICE_PLUGGED_USEC;
static char * const SPA_KEY_DEVICE_BUS_ID;
static char * const SPA_KEY_DEVICE_BUS_PATH;
static char * const SPA_KEY_DEVICE_BUS;
static char * const SPA_KEY_DEVICE_SUBSYSTEM;
static char * const SPA_KEY_DEVICE_SYSFS_PATH;
static char * const SPA_KEY_DEVICE_VENDOR_ID;
static char * const SPA_KEY_DEVICE_VENDOR_NAME;
static char * const SPA_KEY_DEVICE_PRODUCT_ID;
static char * const SPA_KEY_DEVICE_PRODUCT_NAME;
static char * const SPA_KEY_DEVICE_SERIAL;
static char * const SPA_KEY_DEVICE_CLASS;
static char * const SPA_KEY_DEVICE_CAPABILITIES;
static char * const SPA_KEY_DEVICE_FORM_FACTOR;
static char * const SPA_KEY_DEVICE_PROFILE;
static char * const SPA_KEY_DEVICE_PROFILE_SET;
static char * const SPA_KEY_DEVICE_STRING;
int spa_device_add_listener(struct spa_device *d, struct spa_hook *listener, const struct spa_device_events *events, void *data);
int spa_device_sync(struct spa_device *d, int seq);
int spa_device_enum_params(struct spa_device *d, int seq, uint32_t id, uint32_t index, uint32_t max, const struct spa_pod *filter);
int spa_device_set_param(struct spa_device *d, uint32_t id, uint32_t flags, const struct spa_pod *param);

extern "Python" {
    void py_cb_spa_device_event_info(void *data, const struct spa_device_info *info);
    void py_cb_spa_device_event_result(void *data, int seq, int res, uint32_t type, const void *result);
    void py_cb_spa_device_event_event(void *data, const struct spa_event *event);
    void py_cb_spa_device_event_object_info(void *data, uint32_t id, const struct spa_device_object_info *info);
}
"""

# XXX: SPA_DEVICE_EVENT_INIT(id)
SOURCE += """
#include <spa/monitor/event.h>
"""
CDEF += """
enum spa_device_event {
    SPA_DEVICE_EVENT_ObjectConfig,
};
enum spa_event_device {
    SPA_EVENT_DEVICE_START,
    SPA_EVENT_DEVICE_Object,
    SPA_EVENT_DEVICE_Props,
};

uint32_t SPA_DEVICE_EVENT_ID(struct spa_event *ev);
"""

SOURCE += """
#include <spa/monitor/type-info.h>
"""
CDEF += """
static char * const SPA_TYPE_INFO_DeviceEvent;
static char * const SPA_TYPE_INFO_DEVICE_EVENT_BASE;
static char * const SPA_TYPE_INFO_DeviceEventId;
static char * const SPA_TYPE_INFO_DEVICE_EVENT_ID_BASE;

static const struct spa_type_info spa_type_device_event_id[...];
static const struct spa_type_info spa_type_device_event[...];
"""

SOURCE += """
#include <spa/monitor/utils.h>
"""
CDEF += """
struct spa_result_device_params_data {
    struct spa_pod_builder *builder;
    struct spa_result_device_params data;
};

void spa_device_emit_info(struct spa_hook_list *hooks, const struct spa_device_info *i);
void spa_device_emit_result(struct spa_hook_list *hooks, int s, int r, uint32_t t, const void *res);
void spa_device_emit_event(struct spa_hook_list *hooks, const struct spa_event *e);
void spa_device_emit_object_info(struct spa_hook_list *hooks, uint32_t id, const struct spa_device_object_info *i);

static inline void spa_result_func_device_params(void *data, int seq, int res, uint32_t type, const void *result);
static inline int spa_device_enum_params_sync(struct spa_device *device, uint32_t id, uint32_t *index, const struct spa_pod *filter, struct spa_pod **param, struct spa_pod_builder *builder);
"""


# XXX: SPA_NODE_COMMAND_INIT(id)
SOURCE += """
#include <spa/node/command.h>
"""
CDEF += """
enum spa_node_command {
    SPA_NODE_COMMAND_Suspend,
    SPA_NODE_COMMAND_Pause,
    SPA_NODE_COMMAND_Start,
    SPA_NODE_COMMAND_Enable,
    SPA_NODE_COMMAND_Disable,
    SPA_NODE_COMMAND_Flush,
    SPA_NODE_COMMAND_Drain,
    SPA_NODE_COMMAND_Marker,
    SPA_NODE_COMMAND_ParamBegin,
    SPA_NODE_COMMAND_ParamEnd,
};

uint32_t SPA_NODE_COMMAND_ID(struct spa_command *cmd);
"""

# XXX: SPA_NODE_EVENT_INIT(id)
SOURCE += """
#include <spa/node/event.h>
"""
CDEF += """
enum spa_node_event {
    SPA_NODE_EVENT_Error,
    SPA_NODE_EVENT_Buffering,
    SPA_NODE_EVENT_RequestRefresh,
};

uint32_t SPA_NODE_EVENT_ID(struct spa_event *ev);
"""

# XXX: SPA_IO_BUFFERS_INIT, SPA_IO_MEMORY_INIT
SOURCE += """
#include <spa/node/io.h>
"""
CDEF += """
enum spa_io_type {
    SPA_IO_Invalid,
    SPA_IO_Buffers,
    SPA_IO_Range,
    SPA_IO_Clock,
    SPA_IO_Latency,
    SPA_IO_Control,
    SPA_IO_Notify,
    SPA_IO_Position,
    SPA_IO_RateMatch,
    SPA_IO_Memory,
};
struct spa_io_buffers {
    int32_t status;
    uint32_t buffer_id;
};
struct spa_io_memory {
    int32_t status;
    uint32_t size;
    void *data;
};
struct spa_io_range {
    uint64_t offset;
    uint32_t min_size;
    uint32_t max_size;
};
struct spa_io_clock {
    uint32_t flags;
    uint32_t id;
    char name[64];
    uint64_t nsec;
    struct spa_fraction rate;
    uint64_t position;
    uint64_t duration;
    int64_t delay;
    double rate_diff;
    uint64_t next_nsec;
    uint32_t padding[8];
};
struct spa_io_video_size {
    uint32_t flags;
    uint32_t stride;
    struct spa_rectangle size;
    struct spa_fraction framerate;
    uint32_t padding[4];
};
struct spa_io_latency {
    struct spa_fraction rate;
    uint64_t min;
    uint64_t max;
};
struct spa_io_sequence {
    struct spa_pod_sequence sequence;
};
struct spa_io_segment_bar {
    uint32_t flags;
    uint32_t offset;
    float signature_num;
    float signature_denom;
    double bpm;
    double beat;
    uint32_t padding[8];
};
struct spa_io_segment_video {
    uint32_t flags;
    uint32_t offset;
    struct spa_fraction framerate;
    uint32_t hours;
    uint32_t minutes;
    uint32_t seconds;
    uint32_t frames;
    uint32_t field_count;
    uint32_t padding[11];
};
struct spa_io_segment {
    uint32_t version;
    uint32_t flags;
    uint64_t start;
    uint64_t duration;
    double rate;
    uint64_t position;
    struct spa_io_segment_bar bar;
    struct spa_io_segment_video video;
};
enum spa_io_position_state {
    SPA_IO_POSITION_STATE_STOPPED,
    SPA_IO_POSITION_STATE_STARTING,
    SPA_IO_POSITION_STATE_RUNNING,
};
struct spa_io_position {
    struct spa_io_clock clock;
    struct spa_io_video_size video;
    int64_t offset;
    uint32_t state;
    uint32_t n_segments;
    struct spa_io_segment segments[...];
};
struct spa_io_rate_match {
    uint32_t delay;
    uint32_t size;
    double rate;
    uint32_t flags;
    uint32_t padding[7];
};

static const int SPA_STATUS_OK;
static const int SPA_STATUS_NEED_DATA;
static const int SPA_STATUS_HAVE_DATA;
static const int SPA_STATUS_STOPPED;
static const int SPA_STATUS_DRAINED;
static const int SPA_IO_CLOCK_FLAG_FREEWHEEL;
static const int SPA_IO_VIDEO_SIZE_VALID;
static const int SPA_IO_SEGMENT_BAR_FLAG_VALID;
static const int SPA_IO_SEGMENT_VIDEO_FLAG_VALID;
static const int SPA_IO_SEGMENT_VIDEO_FLAG_DROP_FRAME;
static const int SPA_IO_SEGMENT_VIDEO_FLAG_PULL_DOWN;
static const int SPA_IO_SEGMENT_VIDEO_FLAG_INTERLACED;
static const int SPA_IO_SEGMENT_FLAG_LOOPING;
static const int SPA_IO_SEGMENT_FLAG_NO_POSITION;
static const int SPA_IO_POSITION_MAX_SEGMENTS;
static const int SPA_IO_RATE_MATCH_FLAG_ACTIVE;
"""

SOURCE += """
#include <spa/node/keys.h>
"""
CDEF += """
static char * const SPA_KEY_NODE_NAME;
static char * const SPA_KEY_NODE_LATENCY;
static char * const SPA_KEY_NODE_MAX_LATENCY;
static char * const SPA_KEY_NODE_DRIVER;
static char * const SPA_KEY_NODE_ALWAYS_PROCESS;
static char * const SPA_KEY_NODE_PAUSE_ON_IDLE;
static char * const SPA_KEY_NODE_MONITOR;
static char * const SPA_KEY_PORT_NAME;
static char * const SPA_KEY_PORT_ALIAS;
static char * const SPA_KEY_PORT_MONITOR;
"""

# XXX: SPA_NODE_INFO_INIT(), SPA_PORT_INFO_INIT()
SOURCE += """
#include <spa/node/node.h>
"""
CDEF += """
struct spa_node {
    struct spa_interface iface;
};
struct spa_node_info {
    uint32_t max_input_ports;
    uint32_t max_output_ports;
    uint64_t change_mask;
    uint64_t flags;
    struct spa_dict *props;
    struct spa_param_info *params;
    uint32_t n_params;
};
struct spa_port_info {
    uint64_t change_mask;
    uint64_t flags;
    struct spa_fraction rate;
    const struct spa_dict *props;
    struct spa_param_info *params;
    uint32_t n_params;
};
struct spa_result_node_error {
    const char *message;
};
struct spa_result_node_params {
    uint32_t id;
    uint32_t index;
    uint32_t next;
    struct spa_pod *param;
};
struct spa_node_events {
    uint32_t version;
    void (*info) (void *data, const struct spa_node_info *info);
    void (*port_info) (void *data, enum spa_direction direction, uint32_t port, const struct spa_port_info *info);
    void (*result) (void *data, int seq, int res, uint32_t type, const void *result);
    void (*event) (void *data, const struct spa_event *event);
};
struct spa_node_callbacks {
    uint32_t version;
    int (*ready) (void *data, int state);
    int (*reuse_buffer) (void *data, uint32_t port_id, uint32_t buffer_id);
    int (*xrun) (void *data, uint64_t trigger, uint64_t delay, struct spa_pod *info);
};
struct spa_node_methods {
    uint32_t version;
    int (*add_listener) (void *object, struct spa_hook *listener, const struct spa_node_events *events, void *data);
    int (*set_callbacks) (void *object, const struct spa_node_callbacks *callbacks, void *data);
    int (*sync) (void *object, int seq);
    int (*enum_params) (void *object, int seq, uint32_t id, uint32_t start, uint32_t max, const struct spa_pod *filter);
    int (*set_param) (void *object, uint32_t id, uint32_t flags, const struct spa_pod *param);
    int (*set_io) (void *object, uint32_t id, void *data, size_t size);
    int (*send_command) (void *object, const struct spa_command *command);
    int (*add_port) (void *object, enum spa_direction direction, uint32_t port_id, const struct spa_dict *props);
    int (*remove_port) (void *object, enum spa_direction direction, uint32_t port_id);
    int (*port_enum_params) (void *object, int seq, enum spa_direction direction, uint32_t port_id, uint32_t id, uint32_t start, uint32_t max, const struct spa_pod *filter);
    int (*port_set_param) (void *object, enum spa_direction direction, uint32_t port_id, uint32_t id, uint32_t flags, const struct spa_pod *param);
    int (*port_use_buffers) (void *object, enum spa_direction direction, uint32_t port_id, uint32_t flags, struct spa_buffer **buffers, uint32_t n_buffers);
    int (*port_set_io) (void *object, enum spa_direction direction, uint32_t port_id, uint32_t id, void *data, size_t size);
    int (*port_reuse_buffer) (void *object, uint32_t port_id, uint32_t buffer_id);
    int (*process) (void *object);
};

static char * const SPA_TYPE_INTERFACE_Node;
static const int SPA_VERSION_NODE;
static const int SPA_NODE_CHANGE_MASK_FLAGS;
static const int SPA_NODE_CHANGE_MASK_PROPS;
static const int SPA_NODE_CHANGE_MASK_PARAMS;
static const int SPA_NODE_FLAG_RT;
static const int SPA_NODE_FLAG_IN_DYNAMIC_PORTS;
static const int SPA_NODE_FLAG_OUT_DYNAMIC_PORTS;
static const int SPA_NODE_FLAG_IN_PORT_CONFIG;
static const int SPA_NODE_FLAG_OUT_PORT_CONFIG;
static const int SPA_NODE_FLAG_NEED_CONFIGURE;
static const int SPA_NODE_FLAG_ASYNC;
static const int SPA_PORT_CHANGE_MASK_FLAGS;
static const int SPA_PORT_CHANGE_MASK_RATE;
static const int SPA_PORT_CHANGE_MASK_PROPS;
static const int SPA_PORT_CHANGE_MASK_PARAMS;
static const int SPA_PORT_FLAG_REMOVABLE;
static const int SPA_PORT_FLAG_OPTIONAL;
static const int SPA_PORT_FLAG_CAN_ALLOC_BUFFERS;
static const int SPA_PORT_FLAG_IN_PLACE;
static const int SPA_PORT_FLAG_NO_REF;
static const int SPA_PORT_FLAG_LIVE;
static const int SPA_PORT_FLAG_PHYSICAL;
static const int SPA_PORT_FLAG_TERMINAL;
static const int SPA_PORT_FLAG_DYNAMIC_DATA;
static const int SPA_RESULT_TYPE_NODE_ERROR;
static const int SPA_RESULT_TYPE_NODE_PARAMS;
static const int SPA_NODE_EVENT_INFO;
static const int SPA_NODE_EVENT_PORT_INFO;
static const int SPA_NODE_EVENT_RESULT;
static const int SPA_NODE_EVENT_EVENT;
static const int SPA_NODE_EVENT_NUM;
static const int SPA_VERSION_NODE_EVENTS;
static const int SPA_NODE_CALLBACK_READY;
static const int SPA_NODE_CALLBACK_REUSE_BUFFER;
static const int SPA_NODE_CALLBACK_XRUN;
static const int SPA_NODE_CALLBACK_NUM;
static const int SPA_VERSION_NODE_CALLBACKS;
static const int SPA_NODE_PARAM_FLAG_TEST_ONLY;
static const int SPA_NODE_PARAM_FLAG_FIXATE;
static const int SPA_NODE_PARAM_FLAG_NEAREST;
static const int SPA_NODE_BUFFERS_FLAG_ALLOC;
static const int SPA_NODE_METHOD_ADD_LISTENER;
static const int SPA_NODE_METHOD_SET_CALLBACKS;
static const int SPA_NODE_METHOD_SYNC;
static const int SPA_NODE_METHOD_ENUM_PARAMS;
static const int SPA_NODE_METHOD_SET_PARAM;
static const int SPA_NODE_METHOD_SET_IO;
static const int SPA_NODE_METHOD_SEND_COMMAND;
static const int SPA_NODE_METHOD_ADD_PORT;
static const int SPA_NODE_METHOD_REMOVE_PORT;
static const int SPA_NODE_METHOD_PORT_ENUM_PARAMS;
static const int SPA_NODE_METHOD_PORT_SET_PARAM;
static const int SPA_NODE_METHOD_PORT_USE_BUFFERS;
static const int SPA_NODE_METHOD_PORT_SET_IO;
static const int SPA_NODE_METHOD_PORT_REUSE_BUFFER;
static const int SPA_NODE_METHOD_PROCESS;
static const int SPA_NODE_METHOD_NUM;
static const int SPA_VERSION_NODE_METHODS;
int spa_node_add_listener(struct spa_node *n, struct spa_hook *listener, const struct spa_node_events *events, void *data);
int spa_node_set_callbacks(struct spa_node *n, const struct spa_node_callbacks *callbacks, void *data);
int spa_node_sync(struct spa_node *n, int seq);
int spa_node_enum_params(struct spa_node *n, int seq, uint32_t id, uint32_t start, uint32_t max, const struct spa_pod *filter);
int spa_node_set_param(struct spa_node *n, uint32_t id, uint32_t flags, const struct spa_pod *param);
int spa_node_set_io(struct spa_node *n, uint32_t id, void *data, size_t size);
int spa_node_send_command(struct spa_node *n, const struct spa_command *command);
int spa_node_add_port(struct spa_node *n, enum spa_direction direction, uint32_t port_id, const struct spa_dict *props);
int spa_node_remove_port(struct spa_node *n, enum spa_direction direction, uint32_t port_id);
int spa_node_port_enum_params(struct spa_node *n, int seq, enum spa_direction direction, uint32_t port_id, uint32_t id, uint32_t start, uint32_t max, const struct spa_pod *filter);
int spa_node_port_set_param(struct spa_node *n, enum spa_direction direction, uint32_t port_id, uint32_t id, uint32_t flags, const struct spa_pod *param);
int spa_node_port_use_buffers(struct spa_node *n, enum spa_direction direction, uint32_t port_id, uint32_t flags, struct spa_buffer **buffers, uint32_t n_buffers);
int spa_node_port_set_io(struct spa_node *n, enum spa_direction direction, uint32_t port_id, uint32_t id, void *data, size_t size);
int spa_node_port_reuse_buffer(struct spa_node *n, uint32_t port_id, uint32_t buffer_id);
int spa_node_process(struct spa_node *n);

extern "Python" {
    int py_cb_spa_node_callback_ready(void *data, int state);
    int py_cb_spa_node_callback_reuse_buffer(void *data, uint32_t port_id, uint32_t buffer_id);
    int py_cb_spa_node_callback_xrun(void *data, uint64_t trigger, uint64_t delay, struct spa_pod *info);
    void py_cb_spa_node_event_info(void *data, const struct spa_node_info *info);
    void py_cb_spa_node_event_port_info(void *data, enum spa_direction direction, uint32_t port, const struct spa_port_info *info);
    void py_cb_spa_node_event_result(void *data, int seq, int res, uint32_t type, const void *result);
    void py_cb_spa_node_event_event(void *data, const struct spa_event *event);
}
"""

SOURCE += """
#include <spa/node/type-info.h>
"""
CDEF += """
static char * const SPA_TYPE_INFO_IO;
static char * const SPA_TYPE_INFO_IO_BASE;
static char * const SPA_TYPE_INFO_NodeEvent;
static char * const SPA_TYPE_INFO_NODE_EVENT_BASE;
static char * const SPA_TYPE_INFO_NodeCommand;
static char * const SPA_TYPE_INFO_NODE_COMMAND_BASE;

static const struct spa_type_info spa_type_io[...];
static const struct spa_type_info spa_type_node_event_id[...];
static const struct spa_type_info spa_type_node_event[...];
static const struct spa_type_info spa_type_node_command_id[...];
static const struct spa_type_info spa_type_node_command[...];
"""

SOURCE += """
#include <spa/node/utils.h>
"""
CDEF += """
struct spa_result_node_params_data {
    struct spa_pod_builder *builder;
    struct spa_result_node_params data;
};

void spa_node_emit_info(struct spa_hook_list *hooks, const struct spa_node_info *info);
void spa_node_emit_port_info(struct spa_hook_list *hooks, enum spa_direction direction, uint32_t port, const struct spa_port_info *info);
void spa_node_emit_result(struct spa_hook_list *hooks, int seq, int res, uint32_t type, const void *result);
void spa_node_emit_event(struct spa_hook_list *hooks, const struct spa_event *event);
int spa_node_call_ready(struct spa_callbacks *hook, int state);
int spa_node_call_reuse_buffer(struct spa_callbacks *hook, uint32_t port_id, uint32_t buffer_id);
int spa_node_call_xrun(struct spa_callbacks *hook, uint64_t trigger, uint64_t delay, struct spa_pod *info);

void spa_result_func_node_params(void *data, int seq, int res, uint32_t type, const void *result);
int spa_node_enum_params_sync(struct spa_node *node, uint32_t id, uint32_t *index, const struct spa_pod *filter, struct spa_pod **param, struct spa_pod_builder *builder);
int spa_node_port_enum_params_sync(struct spa_node *node, enum spa_direction direction, uint32_t port_id, uint32_t id, uint32_t *index, const struct spa_pod *filter, struct spa_pod **param, struct spa_pod_builder *builder);
"""


SOURCE += """
#include <spa/param/audio/format-utils.h>
"""
CDEF += """
int spa_format_audio_raw_parse(const struct spa_pod *format, struct spa_audio_info_raw *info);
int spa_format_audio_dsp_parse(const struct spa_pod *format, struct spa_audio_info_dsp *info);
int spa_format_audio_iec958_parse(const struct spa_pod *format, struct spa_audio_info_iec958 *info);
struct spa_pod *spa_format_audio_raw_build(struct spa_pod_builder *builder, uint32_t id, struct spa_audio_info_raw *info);
struct spa_pod *spa_format_audio_dsp_build(struct spa_pod_builder *builder, uint32_t id, struct spa_audio_info_dsp *info);
struct spa_pod *spa_format_audio_iec958_build(struct spa_pod_builder *builder, uint32_t id, struct spa_audio_info_iec958 *info);
"""

SOURCE += """
#include <spa/param/audio/format.h>
"""
CDEF += """
struct spa_audio_info {
    uint32_t media_type;
    uint32_t media_subtype;
    union {
        struct spa_audio_info_raw raw;
        struct spa_audio_info_dsp dsp;
        struct spa_audio_info_iec958 iec958;
    } info;
};
"""

# XXX: SPA_AUDIO_INFO_IEC958_INIT(...)
SOURCE += """
#include <spa/param/audio/iec958.h>
"""
CDEF += """
enum spa_audio_iec958_codec {
    SPA_AUDIO_IEC958_CODEC_UNKNOWN,
    SPA_AUDIO_IEC958_CODEC_PCM,
    SPA_AUDIO_IEC958_CODEC_DTS,
    SPA_AUDIO_IEC958_CODEC_AC3,
    SPA_AUDIO_IEC958_CODEC_MPEG,
    SPA_AUDIO_IEC958_CODEC_MPEG2_AAC,
    SPA_AUDIO_IEC958_CODEC_EAC3,
    SPA_AUDIO_IEC958_CODEC_TRUEHD,
    SPA_AUDIO_IEC958_CODEC_DTSHD,
};
struct spa_audio_info_iec958 {
    enum spa_audio_iec958_codec codec;
    uint32_t flags;
    uint32_t rate;
};
"""

# XXX: SPA_AUDIO_LAYOUT_...
SOURCE += """
#include <spa/param/audio/layout.h>
"""
CDEF += """
struct spa_audio_layout_info {
    uint32_t n_channels;
    uint32_t position[...];
};
"""

# XXX: SPA_AUDIO_INFO_RAW_INIT(...), SPA_AUDIO_INFO_DSP_INIT(...)
SOURCE += """
#include <spa/param/audio/raw.h>
"""
CDEF += """
enum spa_audio_format {
    SPA_AUDIO_FORMAT_UNKNOWN,
    SPA_AUDIO_FORMAT_ENCODED,
    SPA_AUDIO_FORMAT_START_Interleaved,
    SPA_AUDIO_FORMAT_S8,
    SPA_AUDIO_FORMAT_U8,
    SPA_AUDIO_FORMAT_S16_LE,
    SPA_AUDIO_FORMAT_S16_BE,
    SPA_AUDIO_FORMAT_U16_LE,
    SPA_AUDIO_FORMAT_U16_BE,
    SPA_AUDIO_FORMAT_S24_32_LE,
    SPA_AUDIO_FORMAT_S24_32_BE,
    SPA_AUDIO_FORMAT_U24_32_LE,
    SPA_AUDIO_FORMAT_U24_32_BE,
    SPA_AUDIO_FORMAT_S32_LE,
    SPA_AUDIO_FORMAT_S32_BE,
    SPA_AUDIO_FORMAT_U32_LE,
    SPA_AUDIO_FORMAT_U32_BE,
    SPA_AUDIO_FORMAT_S24_LE,
    SPA_AUDIO_FORMAT_S24_BE,
    SPA_AUDIO_FORMAT_U24_LE,
    SPA_AUDIO_FORMAT_U24_BE,
    SPA_AUDIO_FORMAT_S20_LE,
    SPA_AUDIO_FORMAT_S20_BE,
    SPA_AUDIO_FORMAT_U20_LE,
    SPA_AUDIO_FORMAT_U20_BE,
    SPA_AUDIO_FORMAT_S18_LE,
    SPA_AUDIO_FORMAT_S18_BE,
    SPA_AUDIO_FORMAT_U18_LE,
    SPA_AUDIO_FORMAT_U18_BE,
    SPA_AUDIO_FORMAT_F32_LE,
    SPA_AUDIO_FORMAT_F32_BE,
    SPA_AUDIO_FORMAT_F64_LE,
    SPA_AUDIO_FORMAT_F64_BE,
    SPA_AUDIO_FORMAT_ULAW,
    SPA_AUDIO_FORMAT_ALAW,
    SPA_AUDIO_FORMAT_START_Planar,
    SPA_AUDIO_FORMAT_U8P,
    SPA_AUDIO_FORMAT_S16P,
    SPA_AUDIO_FORMAT_S24_32P,
    SPA_AUDIO_FORMAT_S32P,
    SPA_AUDIO_FORMAT_S24P,
    SPA_AUDIO_FORMAT_F32P,
    SPA_AUDIO_FORMAT_F64P,
    SPA_AUDIO_FORMAT_S8P,
    SPA_AUDIO_FORMAT_START_Other,
    SPA_AUDIO_FORMAT_DSP_S32,
    SPA_AUDIO_FORMAT_DSP_F32,
    SPA_AUDIO_FORMAT_DSP_F64,
    SPA_AUDIO_FORMAT_S16,
    SPA_AUDIO_FORMAT_U16,
    SPA_AUDIO_FORMAT_S24_32,
    SPA_AUDIO_FORMAT_U24_32,
    SPA_AUDIO_FORMAT_S32,
    SPA_AUDIO_FORMAT_U32,
    SPA_AUDIO_FORMAT_S24,
    SPA_AUDIO_FORMAT_U24,
    SPA_AUDIO_FORMAT_S20,
    SPA_AUDIO_FORMAT_U20,
    SPA_AUDIO_FORMAT_S18,
    SPA_AUDIO_FORMAT_U18,
    SPA_AUDIO_FORMAT_F32,
    SPA_AUDIO_FORMAT_F64,
    SPA_AUDIO_FORMAT_S16_OE,
    SPA_AUDIO_FORMAT_U16_OE,
    SPA_AUDIO_FORMAT_S24_32_OE,
    SPA_AUDIO_FORMAT_U24_32_OE,
    SPA_AUDIO_FORMAT_S32_OE,
    SPA_AUDIO_FORMAT_U32_OE,
    SPA_AUDIO_FORMAT_S24_OE,
    SPA_AUDIO_FORMAT_U24_OE,
    SPA_AUDIO_FORMAT_S20_OE,
    SPA_AUDIO_FORMAT_U20_OE,
    SPA_AUDIO_FORMAT_S18_OE,
    SPA_AUDIO_FORMAT_U18_OE,
    SPA_AUDIO_FORMAT_F32_OE,
    SPA_AUDIO_FORMAT_F64_OE,
};
enum spa_audio_channel {
    SPA_AUDIO_CHANNEL_UNKNOWN,
    SPA_AUDIO_CHANNEL_NA,
    SPA_AUDIO_CHANNEL_MONO,
    SPA_AUDIO_CHANNEL_FL,
    SPA_AUDIO_CHANNEL_FR,
    SPA_AUDIO_CHANNEL_FC,
    SPA_AUDIO_CHANNEL_LFE,
    SPA_AUDIO_CHANNEL_SL,
    SPA_AUDIO_CHANNEL_SR,
    SPA_AUDIO_CHANNEL_FLC,
    SPA_AUDIO_CHANNEL_FRC,
    SPA_AUDIO_CHANNEL_RC,
    SPA_AUDIO_CHANNEL_RL,
    SPA_AUDIO_CHANNEL_RR,
    SPA_AUDIO_CHANNEL_TC,
    SPA_AUDIO_CHANNEL_TFL,
    SPA_AUDIO_CHANNEL_TFC,
    SPA_AUDIO_CHANNEL_TFR,
    SPA_AUDIO_CHANNEL_TRL,
    SPA_AUDIO_CHANNEL_TRC,
    SPA_AUDIO_CHANNEL_TRR,
    SPA_AUDIO_CHANNEL_RLC,
    SPA_AUDIO_CHANNEL_RRC,
    SPA_AUDIO_CHANNEL_FLW,
    SPA_AUDIO_CHANNEL_FRW,
    SPA_AUDIO_CHANNEL_LFE2,
    SPA_AUDIO_CHANNEL_FLH,
    SPA_AUDIO_CHANNEL_FCH,
    SPA_AUDIO_CHANNEL_FRH,
    SPA_AUDIO_CHANNEL_TFLC,
    SPA_AUDIO_CHANNEL_TFRC,
    SPA_AUDIO_CHANNEL_TSL,
    SPA_AUDIO_CHANNEL_TSR,
    SPA_AUDIO_CHANNEL_LLFE,
    SPA_AUDIO_CHANNEL_RLFE,
    SPA_AUDIO_CHANNEL_BC,
    SPA_AUDIO_CHANNEL_BLC,
    SPA_AUDIO_CHANNEL_BRC,
    SPA_AUDIO_CHANNEL_START_Aux,
    SPA_AUDIO_CHANNEL_AUX0,
    SPA_AUDIO_CHANNEL_AUX1,
    SPA_AUDIO_CHANNEL_AUX2,
    SPA_AUDIO_CHANNEL_AUX3,
    SPA_AUDIO_CHANNEL_AUX4,
    SPA_AUDIO_CHANNEL_AUX5,
    SPA_AUDIO_CHANNEL_AUX6,
    SPA_AUDIO_CHANNEL_AUX7,
    SPA_AUDIO_CHANNEL_AUX8,
    SPA_AUDIO_CHANNEL_AUX9,
    SPA_AUDIO_CHANNEL_AUX10,
    SPA_AUDIO_CHANNEL_AUX11,
    SPA_AUDIO_CHANNEL_AUX12,
    SPA_AUDIO_CHANNEL_AUX13,
    SPA_AUDIO_CHANNEL_AUX14,
    SPA_AUDIO_CHANNEL_AUX15,
    SPA_AUDIO_CHANNEL_AUX16,
    SPA_AUDIO_CHANNEL_AUX17,
    SPA_AUDIO_CHANNEL_AUX18,
    SPA_AUDIO_CHANNEL_AUX19,
    SPA_AUDIO_CHANNEL_AUX20,
    SPA_AUDIO_CHANNEL_AUX21,
    SPA_AUDIO_CHANNEL_AUX22,
    SPA_AUDIO_CHANNEL_AUX23,
    SPA_AUDIO_CHANNEL_AUX24,
    SPA_AUDIO_CHANNEL_AUX25,
    SPA_AUDIO_CHANNEL_AUX26,
    SPA_AUDIO_CHANNEL_AUX27,
    SPA_AUDIO_CHANNEL_AUX28,
    SPA_AUDIO_CHANNEL_AUX29,
    SPA_AUDIO_CHANNEL_AUX30,
    SPA_AUDIO_CHANNEL_AUX31,
    SPA_AUDIO_CHANNEL_AUX32,
    SPA_AUDIO_CHANNEL_AUX33,
    SPA_AUDIO_CHANNEL_AUX34,
    SPA_AUDIO_CHANNEL_AUX35,
    SPA_AUDIO_CHANNEL_AUX36,
    SPA_AUDIO_CHANNEL_AUX37,
    SPA_AUDIO_CHANNEL_AUX38,
    SPA_AUDIO_CHANNEL_AUX39,
    SPA_AUDIO_CHANNEL_AUX40,
    SPA_AUDIO_CHANNEL_AUX41,
    SPA_AUDIO_CHANNEL_AUX42,
    SPA_AUDIO_CHANNEL_AUX43,
    SPA_AUDIO_CHANNEL_AUX44,
    SPA_AUDIO_CHANNEL_AUX45,
    SPA_AUDIO_CHANNEL_AUX46,
    SPA_AUDIO_CHANNEL_AUX47,
    SPA_AUDIO_CHANNEL_AUX48,
    SPA_AUDIO_CHANNEL_AUX49,
    SPA_AUDIO_CHANNEL_AUX50,
    SPA_AUDIO_CHANNEL_AUX51,
    SPA_AUDIO_CHANNEL_AUX52,
    SPA_AUDIO_CHANNEL_AUX53,
    SPA_AUDIO_CHANNEL_AUX54,
    SPA_AUDIO_CHANNEL_AUX55,
    SPA_AUDIO_CHANNEL_AUX56,
    SPA_AUDIO_CHANNEL_AUX57,
    SPA_AUDIO_CHANNEL_AUX58,
    SPA_AUDIO_CHANNEL_AUX59,
    SPA_AUDIO_CHANNEL_AUX60,
    SPA_AUDIO_CHANNEL_AUX61,
    SPA_AUDIO_CHANNEL_AUX62,
    SPA_AUDIO_CHANNEL_AUX63,
    SPA_AUDIO_CHANNEL_LAST_Aux,
    SPA_AUDIO_CHANNEL_START_Custom,
};
struct spa_audio_info_raw {
    enum spa_audio_format format;
    uint32_t flags;
    uint32_t rate;
    uint32_t channels;
    uint32_t position[...];
};
struct spa_audio_info_dsp {
    enum spa_audio_format format;
};

static const int SPA_AUDIO_MAX_CHANNELS;
static const int SPA_AUDIO_FLAG_NONE;
static const int SPA_AUDIO_FLAG_UNPOSITIONED;
static char * const SPA_KEY_AUDIO_FORMAT;
static char * const SPA_KEY_AUDIO_CHANNEL;
static char * const SPA_KEY_AUDIO_CHANNELS;
static char * const SPA_KEY_AUDIO_RATE;
static char * const SPA_KEY_AUDIO_POSITION;
bool SPA_AUDIO_FORMAT_IS_INTERLEAVED(enum spa_audio_format fmt);
bool SPA_AUDIO_FORMAT_IS_PLANAR(enum spa_audio_format fmt);
"""

SOURCE += """
#include <spa/param/audio/type-info.h>
"""
CDEF += """
static char * const SPA_TYPE_INFO_AudioFormat;
static char * const SPA_TYPE_INFO_AUDIO_FORMAT_BASE;
static char * const SPA_TYPE_INFO_AudioFlags;
static char * const SPA_TYPE_INFO_AUDIO_FLAGS_BASE;
static char * const SPA_TYPE_INFO_AudioChannel;
static char * const SPA_TYPE_INFO_AUDIO_CHANNEL_BASE;
static char * const SPA_TYPE_INFO_AudioIEC958Codec;
static char * const SPA_TYPE_INFO_AUDIO_IEC958_CODEC_BASE;

static const struct spa_type_info spa_type_audio_format[...];
static const struct spa_type_info spa_type_audio_flags[...];
static const struct spa_type_info spa_type_audio_channel[...];
static const struct spa_type_info spa_type_audio_iec958_codec[...];
"""

SOURCE += """
#include <spa/param/bluetooth/audio.h>
"""
CDEF += """
enum spa_bluetooth_audio_codec {
    SPA_BLUETOOTH_AUDIO_CODEC_START,
    SPA_BLUETOOTH_AUDIO_CODEC_SBC,
    SPA_BLUETOOTH_AUDIO_CODEC_SBC_XQ,
    SPA_BLUETOOTH_AUDIO_CODEC_MPEG,
    SPA_BLUETOOTH_AUDIO_CODEC_AAC,
    SPA_BLUETOOTH_AUDIO_CODEC_APTX,
    SPA_BLUETOOTH_AUDIO_CODEC_APTX_HD,
    SPA_BLUETOOTH_AUDIO_CODEC_LDAC,
    SPA_BLUETOOTH_AUDIO_CODEC_APTX_LL,
    SPA_BLUETOOTH_AUDIO_CODEC_APTX_LL_DUPLEX,
    SPA_BLUETOOTH_AUDIO_CODEC_FASTSTREAM,
    SPA_BLUETOOTH_AUDIO_CODEC_FASTSTREAM_DUPLEX,
    SPA_BLUETOOTH_AUDIO_CODEC_CVSD,,
    SPA_BLUETOOTH_AUDIO_CODEC_MSBC,
};
"""

SOURCE += """
#include <spa/param/bluetooth/type-info.h>
"""
CDEF += """
static char * const SPA_TYPE_INFO_BluetoothAudioCodec;
static char * const SPA_TYPE_INFO_BLUETOOTH_AUDIO_CODEC_BASE;

static const struct spa_type_info spa_type_bluetooth_audio_codec[...];
"""

SOURCE += """
#include <spa/param/video/chroma.h>
"""
CDEF += """
enum spa_video_chroma_site {
    SPA_VIDEO_CHROMA_SITE_UNKNOWN,
    SPA_VIDEO_CHROMA_SITE_NONE,
    SPA_VIDEO_CHROMA_SITE_H_COSITED,
    SPA_VIDEO_CHROMA_SITE_V_COSITED,
    SPA_VIDEO_CHROMA_SITE_ALT_LINE,
    SPA_VIDEO_CHROMA_SITE_COSITED,
    SPA_VIDEO_CHROMA_SITE_JPEG,
    SPA_VIDEO_CHROMA_SITE_MPEG2,
    SPA_VIDEO_CHROMA_SITE_DV,
};
"""

SOURCE += """
#include <spa/param/video/color.h>
"""
CDEF += """
enum spa_video_color_range {
    SPA_VIDEO_COLOR_RANGE_UNKNOWN,
    SPA_VIDEO_COLOR_RANGE_0_255,
    SPA_VIDEO_COLOR_RANGE_16_235,
};
enum spa_video_color_matrix {
    SPA_VIDEO_COLOR_MATRIX_UNKNOWN,
    SPA_VIDEO_COLOR_MATRIX_RGB,
    SPA_VIDEO_COLOR_MATRIX_FCC,
    SPA_VIDEO_COLOR_MATRIX_BT709,
    SPA_VIDEO_COLOR_MATRIX_BT601,
    SPA_VIDEO_COLOR_MATRIX_SMPTE240M,
    SPA_VIDEO_COLOR_MATRIX_BT2020,
};
enum spa_video_transfer_function {
    SPA_VIDEO_TRANSFER_UNKNOWN,
    SPA_VIDEO_TRANSFER_GAMMA10,
    SPA_VIDEO_TRANSFER_GAMMA18,
    SPA_VIDEO_TRANSFER_GAMMA20,
    SPA_VIDEO_TRANSFER_GAMMA22,
    SPA_VIDEO_TRANSFER_BT709,
    SPA_VIDEO_TRANSFER_SMPTE240M,
    SPA_VIDEO_TRANSFER_SRGB,
    SPA_VIDEO_TRANSFER_GAMMA28,
    SPA_VIDEO_TRANSFER_LOG100,
    SPA_VIDEO_TRANSFER_LOG316,
    SPA_VIDEO_TRANSFER_BT2020_12,
    SPA_VIDEO_TRANSFER_ADOBERGB,
};
enum spa_video_color_primaries {
    SPA_VIDEO_COLOR_PRIMARIES_UNKNOWN,
    SPA_VIDEO_COLOR_PRIMARIES_BT709,
    SPA_VIDEO_COLOR_PRIMARIES_BT470M,
    SPA_VIDEO_COLOR_PRIMARIES_BT470BG,
    SPA_VIDEO_COLOR_PRIMARIES_SMPTE170M,
    SPA_VIDEO_COLOR_PRIMARIES_SMPTE240M,
    SPA_VIDEO_COLOR_PRIMARIES_FILM,
    SPA_VIDEO_COLOR_PRIMARIES_BT2020,
    SPA_VIDEO_COLOR_PRIMARIES_ADOBERGB,
};
struct spa_video_colorimetry {
    enum spa_video_color_range range;
    enum spa_video_color_matrix matrix;
    enum spa_video_transfer_function transfer;
    enum spa_video_color_primaries primaries;
};
"""

SOURCE += """
#include <spa/param/video/encoded.h>
"""
CDEF += """
enum spa_h264_stream_format {
    SPA_H264_STREAM_FORMAT_UNKNOWN,
    SPA_H264_STREAM_FORMAT_AVC,
    SPA_H264_STREAM_FORMAT_AVC3,
    SPA_H264_STREAM_FORMAT_BYTESTREAM,
};
enum spa_h264_alignment {
    SPA_H264_ALIGNMENT_UNKNOWN,
    SPA_H264_ALIGNMENT_AU,
    SPA_H264_ALIGNMENT_NAL,
};
struct spa_video_info_h264 {
    struct spa_rectangle size;
    struct spa_fraction framerate;
    struct spa_fraction max_framerate;
    enum spa_h264_stream_format stream_format;
    enum spa_h264_alignment alignment;
};
struct spa_video_info_mjpg {
    struct spa_rectangle size;
    struct spa_fraction framerate;
    struct spa_fraction max_framerate;
};
"""

SOURCE += """
#include <spa/param/video/format-utils.h>
"""
CDEF += """
int spa_format_video_raw_parse(const struct spa_pod *format, struct spa_video_info_raw *info);
int spa_format_video_dsp_parse(const struct spa_pod *format, struct spa_video_info_dsp *info);
struct spa_pod *spa_format_video_raw_build(struct spa_pod_builder *builder, uint32_t id, struct spa_video_info_raw *info);
struct spa_pod *spa_format_video_dsp_build(struct spa_pod_builder *builder, uint32_t id, struct spa_video_info_dsp *info);
int spa_format_video_h264_parse(const struct spa_pod *format, struct spa_video_info_h264 *info);
int spa_format_video_mjpg_parse(const struct spa_pod *format, struct spa_video_info_mjpg *info);
"""

SOURCE += """
#include <spa/param/video/format.h>
"""
CDEF += """
struct spa_video_info {
    uint32_t media_type;
    uint32_t media_subtype;
    union {
        struct spa_video_info_raw raw;
        struct spa_video_info_dsp dsp;
        struct spa_video_info_h264 h264;
        struct spa_video_info_mjpg mjpg;
    } info;
};
"""

SOURCE += """
#include <spa/param/video/multiview.h>
"""
CDEF += """
enum spa_video_multiview_mode {
    SPA_VIDEO_MULTIVIEW_MODE_NONE,
    SPA_VIDEO_MULTIVIEW_MODE_MONO,
    SPA_VIDEO_MULTIVIEW_MODE_LEFT,
    SPA_VIDEO_MULTIVIEW_MODE_RIGHT,
    SPA_VIDEO_MULTIVIEW_MODE_SIDE_BY_SIDE,
    SPA_VIDEO_MULTIVIEW_MODE_SIDE_BY_SIDE_QUINCUNX,
    SPA_VIDEO_MULTIVIEW_MODE_COLUMN_INTERLEAVED,
    SPA_VIDEO_MULTIVIEW_MODE_ROW_INTERLEAVED,
    SPA_VIDEO_MULTIVIEW_MODE_TOP_BOTTOM,
    SPA_VIDEO_MULTIVIEW_MODE_CHECKERBOARD,
    SPA_VIDEO_MULTIVIEW_MODE_FRAME_BY_FRAME,
    SPA_VIDEO_MULTIVIEW_MODE_MULTIVIEW_FRAME_BY_FRAME,
    SPA_VIDEO_MULTIVIEW_MODE_SEPARATED,
};
enum spa_video_multiview_flags {
    SPA_VIDEO_MULTIVIEW_FLAGS_NONE,
    SPA_VIDEO_MULTIVIEW_FLAGS_RIGHT_VIEW_FIRST,
    SPA_VIDEO_MULTIVIEW_FLAGS_LEFT_FLIPPED,
    SPA_VIDEO_MULTIVIEW_FLAGS_LEFT_FLOPPED,
    SPA_VIDEO_MULTIVIEW_FLAGS_RIGHT_FLIPPED,
    SPA_VIDEO_MULTIVIEW_FLAGS_RIGHT_FLOPPED,
    SPA_VIDEO_MULTIVIEW_FLAGS_HALF_ASPECT,
    SPA_VIDEO_MULTIVIEW_FLAGS_MIXED_MONO,
};
"""

# XXX: SPA_VIDEO_INFO_RAW_INIT(...), SPA_VIDEO_INFO_DSP_INIT(...)
SOURCE += """
#include <spa/param/video/raw.h>
"""
CDEF += """
enum spa_video_format {
    SPA_VIDEO_FORMAT_UNKNOWN,
    SPA_VIDEO_FORMAT_ENCODED,
    SPA_VIDEO_FORMAT_I420,
    SPA_VIDEO_FORMAT_YV12,
    SPA_VIDEO_FORMAT_YUY2,
    SPA_VIDEO_FORMAT_UYVY,
    SPA_VIDEO_FORMAT_AYUV,
    SPA_VIDEO_FORMAT_RGBx,
    SPA_VIDEO_FORMAT_BGRx,
    SPA_VIDEO_FORMAT_xRGB,
    SPA_VIDEO_FORMAT_xBGR,
    SPA_VIDEO_FORMAT_RGBA,
    SPA_VIDEO_FORMAT_BGRA,
    SPA_VIDEO_FORMAT_ARGB,
    SPA_VIDEO_FORMAT_ABGR,
    SPA_VIDEO_FORMAT_RGB,
    SPA_VIDEO_FORMAT_BGR,
    SPA_VIDEO_FORMAT_Y41B,
    SPA_VIDEO_FORMAT_Y42B,
    SPA_VIDEO_FORMAT_YVYU,
    SPA_VIDEO_FORMAT_Y444,
    SPA_VIDEO_FORMAT_v210,
    SPA_VIDEO_FORMAT_v216,
    SPA_VIDEO_FORMAT_NV12,
    SPA_VIDEO_FORMAT_NV21,
    SPA_VIDEO_FORMAT_GRAY8,
    SPA_VIDEO_FORMAT_GRAY16_BE,
    SPA_VIDEO_FORMAT_GRAY16_LE,
    SPA_VIDEO_FORMAT_v308,
    SPA_VIDEO_FORMAT_RGB16,
    SPA_VIDEO_FORMAT_BGR16,
    SPA_VIDEO_FORMAT_RGB15,
    SPA_VIDEO_FORMAT_BGR15,
    SPA_VIDEO_FORMAT_UYVP,
    SPA_VIDEO_FORMAT_A420,
    SPA_VIDEO_FORMAT_RGB8P,
    SPA_VIDEO_FORMAT_YUV9,
    SPA_VIDEO_FORMAT_YVU9,
    SPA_VIDEO_FORMAT_IYU1,
    SPA_VIDEO_FORMAT_ARGB64,
    SPA_VIDEO_FORMAT_AYUV64,
    SPA_VIDEO_FORMAT_r210,
    SPA_VIDEO_FORMAT_I420_10BE,
    SPA_VIDEO_FORMAT_I420_10LE,
    SPA_VIDEO_FORMAT_I422_10BE,
    SPA_VIDEO_FORMAT_I422_10LE,
    SPA_VIDEO_FORMAT_Y444_10BE,
    SPA_VIDEO_FORMAT_Y444_10LE,
    SPA_VIDEO_FORMAT_GBR,
    SPA_VIDEO_FORMAT_GBR_10BE,
    SPA_VIDEO_FORMAT_GBR_10LE,
    SPA_VIDEO_FORMAT_NV16,
    SPA_VIDEO_FORMAT_NV24,
    SPA_VIDEO_FORMAT_NV12_64Z32,
    SPA_VIDEO_FORMAT_A420_10BE,
    SPA_VIDEO_FORMAT_A420_10LE,
    SPA_VIDEO_FORMAT_A422_10BE,
    SPA_VIDEO_FORMAT_A422_10LE,
    SPA_VIDEO_FORMAT_A444_10BE,
    SPA_VIDEO_FORMAT_A444_10LE,
    SPA_VIDEO_FORMAT_NV61,
    SPA_VIDEO_FORMAT_P010_10BE,
    SPA_VIDEO_FORMAT_P010_10LE,
    SPA_VIDEO_FORMAT_IYU2,
    SPA_VIDEO_FORMAT_VYUY,
    SPA_VIDEO_FORMAT_GBRA,
    SPA_VIDEO_FORMAT_GBRA_10BE,
    SPA_VIDEO_FORMAT_GBRA_10LE,
    SPA_VIDEO_FORMAT_GBR_12BE,
    SPA_VIDEO_FORMAT_GBR_12LE,
    SPA_VIDEO_FORMAT_GBRA_12BE,
    SPA_VIDEO_FORMAT_GBRA_12LE,
    SPA_VIDEO_FORMAT_I420_12BE,
    SPA_VIDEO_FORMAT_I420_12LE,
    SPA_VIDEO_FORMAT_I422_12BE,
    SPA_VIDEO_FORMAT_I422_12LE,
    SPA_VIDEO_FORMAT_Y444_12BE,
    SPA_VIDEO_FORMAT_Y444_12LE,
    SPA_VIDEO_FORMAT_RGBA_F16,
    SPA_VIDEO_FORMAT_RGBA_F32,
    SPA_VIDEO_FORMAT_DSP_F32,
};
enum spa_video_flags {
    SPA_VIDEO_FLAG_NONE = 0,
    SPA_VIDEO_FLAG_VARIABLE_FPS,
    SPA_VIDEO_FLAG_PREMULTIPLIED_ALPHA,
};
enum spa_video_interlace_mode {
    SPA_VIDEO_INTERLACE_MODE_PROGRESSIVE,
    SPA_VIDEO_INTERLACE_MODE_INTERLEAVED,
    SPA_VIDEO_INTERLACE_MODE_MIXED,
    SPA_VIDEO_INTERLACE_MODE_FIELDS,
};
struct spa_video_info_raw {
    enum spa_video_format format;
    int64_t modifier;
    struct spa_rectangle size;
    struct spa_fraction framerate;
    struct spa_fraction max_framerate;
    uint32_t views;
    enum spa_video_interlace_mode interlace_mode;
    struct spa_fraction pixel_aspect_ratio;
    enum spa_video_multiview_mode multiview_mode;
    enum spa_video_multiview_flags multiview_flags;
    enum spa_video_chroma_site chroma_site;
    enum spa_video_color_range color_range;
    enum spa_video_color_matrix color_matrix;
    enum spa_video_transfer_function transfer_function;
    enum spa_video_color_primaries color_primaries;
};
struct spa_video_info_dsp {
    enum spa_video_format format;
    int64_t modifier;
};
"""

SOURCE += """
#include <spa/param/video/type-info.h>
"""
CDEF += """
static char * const SPA_TYPE_INFO_VideoFormat;
static char * const SPA_TYPE_INFO_VIDEO_FORMAT_BASE;

static const struct spa_type_info spa_type_video_format[...];
"""

SOURCE += """
#include <spa/param/format-utils.h>
"""
CDEF += """
int spa_format_parse(const struct spa_pod *format, uint32_t *media_type, uint32_t *media_subtype);
"""

SOURCE += """
#include <spa/param/format.h>
"""
CDEF += """
enum spa_media_type {
    SPA_MEDIA_TYPE_unknown,
    SPA_MEDIA_TYPE_audio,
    SPA_MEDIA_TYPE_video,
    SPA_MEDIA_TYPE_image,
    SPA_MEDIA_TYPE_binary,
    SPA_MEDIA_TYPE_stream,
    SPA_MEDIA_TYPE_application,
};
enum spa_media_subtype {
    SPA_MEDIA_SUBTYPE_unknown,
    SPA_MEDIA_SUBTYPE_raw,
    SPA_MEDIA_SUBTYPE_dsp,
    SPA_MEDIA_SUBTYPE_iec958,
    SPA_MEDIA_SUBTYPE_START_Audio,
    SPA_MEDIA_SUBTYPE_mp3,
    SPA_MEDIA_SUBTYPE_aac,
    SPA_MEDIA_SUBTYPE_vorbis,
    SPA_MEDIA_SUBTYPE_wma,
    SPA_MEDIA_SUBTYPE_ra,
    SPA_MEDIA_SUBTYPE_sbc,
    SPA_MEDIA_SUBTYPE_adpcm,
    SPA_MEDIA_SUBTYPE_g723,
    SPA_MEDIA_SUBTYPE_g726,
    SPA_MEDIA_SUBTYPE_g729,
    SPA_MEDIA_SUBTYPE_amr,
    SPA_MEDIA_SUBTYPE_gsm,
    SPA_MEDIA_SUBTYPE_START_Video,
    SPA_MEDIA_SUBTYPE_h264,
    SPA_MEDIA_SUBTYPE_mjpg,
    SPA_MEDIA_SUBTYPE_dv,
    SPA_MEDIA_SUBTYPE_mpegts,
    SPA_MEDIA_SUBTYPE_h263,
    SPA_MEDIA_SUBTYPE_mpeg1,
    SPA_MEDIA_SUBTYPE_mpeg2,
    SPA_MEDIA_SUBTYPE_mpeg4,
    SPA_MEDIA_SUBTYPE_xvid,
    SPA_MEDIA_SUBTYPE_vc1,
    SPA_MEDIA_SUBTYPE_vp8,
    SPA_MEDIA_SUBTYPE_vp9,
    SPA_MEDIA_SUBTYPE_bayer,
    SPA_MEDIA_SUBTYPE_START_Image,
    SPA_MEDIA_SUBTYPE_jpeg,
    SPA_MEDIA_SUBTYPE_START_Binary,
    SPA_MEDIA_SUBTYPE_START_Stream,
    SPA_MEDIA_SUBTYPE_midi,
    SPA_MEDIA_SUBTYPE_START_Application,
    SPA_MEDIA_SUBTYPE_control,
};
enum spa_format {
    SPA_FORMAT_START,
    SPA_FORMAT_mediaType,
    SPA_FORMAT_mediaSubtype,
    SPA_FORMAT_START_Audio,
    SPA_FORMAT_AUDIO_format,
    SPA_FORMAT_AUDIO_flags,
    SPA_FORMAT_AUDIO_rate,
    SPA_FORMAT_AUDIO_channels,
    SPA_FORMAT_AUDIO_position,
    SPA_FORMAT_AUDIO_iec958Codec,
    SPA_FORMAT_START_Video,
    SPA_FORMAT_VIDEO_format,
    SPA_FORMAT_VIDEO_modifier,
    SPA_FORMAT_VIDEO_size,
    SPA_FORMAT_VIDEO_framerate,
    SPA_FORMAT_VIDEO_maxFramerate,
    SPA_FORMAT_VIDEO_views,
    SPA_FORMAT_VIDEO_interlaceMode,
    SPA_FORMAT_VIDEO_pixelAspectRatio,
    SPA_FORMAT_VIDEO_multiviewMode,
    SPA_FORMAT_VIDEO_multiviewFlags,
    SPA_FORMAT_VIDEO_chromaSite,
    SPA_FORMAT_VIDEO_colorRange,
    SPA_FORMAT_VIDEO_colorMatrix,
    SPA_FORMAT_VIDEO_transferFunction,
    SPA_FORMAT_VIDEO_colorPrimaries,
    SPA_FORMAT_VIDEO_profile,
    SPA_FORMAT_VIDEO_level,
    SPA_FORMAT_VIDEO_H264_streamFormat,
    SPA_FORMAT_VIDEO_H264_alignment,
    SPA_FORMAT_START_Image,
    SPA_FORMAT_START_Binary,
    SPA_FORMAT_START_Stream,
    SPA_FORMAT_START_Application,
};

static char * const SPA_KEY_FORMAT_DSP;
"""

# XXX: SPA_LATENCY_INFO(dir, ...), SPA_PROCESS_LATENCY_INFO_INIT(...)
SOURCE += """
#include <spa/param/latency-utils.h>
"""
CDEF += """
struct spa_latency_info {
    enum spa_direction direction;
    float min_quantum;
    float max_quantum;
    uint32_t min_rate;
    uint32_t max_rate;
    uint64_t min_ns;
    uint64_t max_ns;
};
struct spa_process_latency_info {
    float quantum;
    uint32_t rate;
    uint64_t ns;
};

int spa_latency_info_compare(const struct spa_latency_info *a, struct spa_latency_info *b);
int spa_latency_info_combine(struct spa_latency_info *info, const struct spa_latency_info *other);
int spa_latency_parse(const struct spa_pod *latency, struct spa_latency_info *info);
struct spa_pod *spa_latency_build(struct spa_pod_builder *builder, uint32_t id, const struct spa_latency_info *info);
int spa_process_latency_parse(const struct spa_pod *latency, struct spa_process_latency_info *info);
struct spa_pod *spa_process_latency_build(struct spa_pod_builder *builder, uint32_t id, const struct spa_process_latency_info *info);
int spa_process_latency_info_add(const struct spa_process_latency_info *process, struct spa_latency_info *info);
"""

# XXX: SPA_PARAM_INFO(id, flags)
SOURCE += """
#include <spa/param/param.h>
"""
CDEF += """
enum spa_param_type {
    SPA_PARAM_Invalid,
    SPA_PARAM_PropInfo,
    SPA_PARAM_Props,
    SPA_PARAM_EnumFormat,
    SPA_PARAM_Format,
    SPA_PARAM_Buffers,
    SPA_PARAM_Meta,
    SPA_PARAM_IO,
    SPA_PARAM_EnumProfile,
    SPA_PARAM_Profile,
    SPA_PARAM_EnumPortConfig,
    SPA_PARAM_PortConfig,
    SPA_PARAM_EnumRoute,
    SPA_PARAM_Route,
    SPA_PARAM_Control,
    SPA_PARAM_Latency,
    SPA_PARAM_ProcessLatency,
};
struct spa_param_info {
    uint32_t id;
    uint32_t flags;
    uint32_t user;
    uint32_t padding[5];
};
enum spa_param_buffers {
    SPA_PARAM_BUFFERS_START,
    SPA_PARAM_BUFFERS_buffers,
    SPA_PARAM_BUFFERS_blocks,
    SPA_PARAM_BUFFERS_size,
    SPA_PARAM_BUFFERS_stride,
    SPA_PARAM_BUFFERS_align,
    SPA_PARAM_BUFFERS_dataType,
};
enum spa_param_meta {
    SPA_PARAM_META_START,
    SPA_PARAM_META_type,
    SPA_PARAM_META_size,
};
enum spa_param_io {
    SPA_PARAM_IO_START,
    SPA_PARAM_IO_id,
    SPA_PARAM_IO_size,
};
enum spa_param_availability {
    SPA_PARAM_AVAILABILITY_unknown,
    SPA_PARAM_AVAILABILITY_no,
    SPA_PARAM_AVAILABILITY_yes,
};
enum spa_param_profile {
    SPA_PARAM_PROFILE_START,
    SPA_PARAM_PROFILE_index,
    SPA_PARAM_PROFILE_name,
    SPA_PARAM_PROFILE_description,
    SPA_PARAM_PROFILE_priority,
    SPA_PARAM_PROFILE_available,
    SPA_PARAM_PROFILE_info,
    SPA_PARAM_PROFILE_classes,
    SPA_PARAM_PROFILE_save,
};
enum spa_param_port_config_mode {
    SPA_PARAM_PORT_CONFIG_MODE_none,
    SPA_PARAM_PORT_CONFIG_MODE_passthrough,
    SPA_PARAM_PORT_CONFIG_MODE_convert,
    SPA_PARAM_PORT_CONFIG_MODE_dsp,
};
enum spa_param_port_config {
    SPA_PARAM_PORT_CONFIG_START,
    SPA_PARAM_PORT_CONFIG_direction,
    SPA_PARAM_PORT_CONFIG_mode,
    SPA_PARAM_PORT_CONFIG_monitor,
    SPA_PARAM_PORT_CONFIG_control,
    SPA_PARAM_PORT_CONFIG_format,
};
enum spa_param_route {
    SPA_PARAM_ROUTE_START,
    SPA_PARAM_ROUTE_index,
    SPA_PARAM_ROUTE_direction,
    SPA_PARAM_ROUTE_device,
    SPA_PARAM_ROUTE_name,
    SPA_PARAM_ROUTE_description,
    SPA_PARAM_ROUTE_priority,
    SPA_PARAM_ROUTE_available,
    SPA_PARAM_ROUTE_info,
    SPA_PARAM_ROUTE_profiles,
    SPA_PARAM_ROUTE_props,
    SPA_PARAM_ROUTE_devices,
    SPA_PARAM_ROUTE_profile,
    SPA_PARAM_ROUTE_save,
};
enum spa_param_latency {
    SPA_PARAM_LATENCY_START,
    SPA_PARAM_LATENCY_direction,
    SPA_PARAM_LATENCY_minQuantum,
    SPA_PARAM_LATENCY_maxQuantum,
    SPA_PARAM_LATENCY_minRate,
    SPA_PARAM_LATENCY_maxRate,
    SPA_PARAM_LATENCY_minNs,
    SPA_PARAM_LATENCY_maxNs,
};
enum spa_param_process_latency {
    SPA_PARAM_PROCESS_LATENCY_START,
    SPA_PARAM_PROCESS_LATENCY_quantum,
    SPA_PARAM_PROCESS_LATENCY_rate,
    SPA_PARAM_PROCESS_LATENCY_ns,
};

static const int SPA_PARAM_INFO_SERIAL;
static const int SPA_PARAM_INFO_READ;
static const int SPA_PARAM_INFO_WRITE;
static const int SPA_PARAM_INFO_READWRITE;
"""

SOURCE += """
#include <spa/param/profiler.h>
"""
CDEF += """
enum spa_profiler {
    SPA_PROFILER_START,
    SPA_PROFILER_START_Driver,
    SPA_PROFILER_info,
    SPA_PROFILER_clock,
    SPA_PROFILER_driverBlock,
    SPA_PROFILER_START_Follower,
    SPA_PROFILER_followerBlock,
    SPA_PROFILER_START_CUSTOM,
};

"""

SOURCE += """
#include <spa/param/props.h>
"""
CDEF += """
enum spa_prop_info {
    SPA_PROP_INFO_START,
    SPA_PROP_INFO_id,
    SPA_PROP_INFO_name,
    SPA_PROP_INFO_type,
    SPA_PROP_INFO_labels,
    SPA_PROP_INFO_container,
    SPA_PROP_INFO_params,
};
enum spa_prop {
    SPA_PROP_START,
    SPA_PROP_unknown,
    SPA_PROP_START_Device,
    SPA_PROP_device,
    SPA_PROP_deviceName,
    SPA_PROP_deviceFd,
    SPA_PROP_card,
    SPA_PROP_cardName,
    SPA_PROP_minLatency,
    SPA_PROP_maxLatency,
    SPA_PROP_periods,
    SPA_PROP_periodSize,
    SPA_PROP_periodEvent,
    SPA_PROP_live,
    SPA_PROP_rate,
    SPA_PROP_quality,
    SPA_PROP_bluetoothAudioCodec,
    SPA_PROP_START_Audio,
    SPA_PROP_waveType,
    SPA_PROP_frequency,
    SPA_PROP_volume,
    SPA_PROP_mute,
    SPA_PROP_patternType,
    SPA_PROP_ditherType,
    SPA_PROP_truncate,
    SPA_PROP_channelVolumes,
    SPA_PROP_volumeBase,
    SPA_PROP_volumeStep,
    SPA_PROP_channelMap,
    SPA_PROP_monitorMute,
    SPA_PROP_monitorVolumes,
    SPA_PROP_latencyOffsetNsec,
    SPA_PROP_softMute,
    SPA_PROP_softVolumes,
    SPA_PROP_iec958Codecs,
    SPA_PROP_START_Video,
    SPA_PROP_brightness,
    SPA_PROP_contrast,
    SPA_PROP_saturation,
    SPA_PROP_hue,
    SPA_PROP_gamma,
    SPA_PROP_exposure,
    SPA_PROP_gain,
    SPA_PROP_sharpness,
    SPA_PROP_START_Other,
    SPA_PROP_params,
    SPA_PROP_START_CUSTOM,
};
"""

SOURCE += """
#include <spa/param/type-info.h>
"""
CDEF += """
static char * const SPA_TYPE_INFO_ParamId;
static char * const SPA_TYPE_INFO_PARAM_ID_BASE;
static char * const SPA_TYPE_INFO_Param;
static char * const SPA_TYPE_INFO_PARAM_BASE;
static char * const SPA_TYPE_INFO_Props;
static char * const SPA_TYPE_INFO_PROPS_BASE;
static char * const SPA_TYPE_INFO_PropInfo;
static char * const SPA_TYPE_INFO_PROP_INFO_BASE;
static char * const SPA_TYPE_INFO_PARAM_Meta;
static char * const SPA_TYPE_INFO_PARAM_META_BASE;
static char * const SPA_TYPE_INFO_PARAM_IO;
static char * const SPA_TYPE_INFO_PARAM_IO_BASE;
static char * const SPA_TYPE_INFO_Format;
static char * const SPA_TYPE_INFO_FORMAT_BASE;
static char * const SPA_TYPE_INFO_MediaType;
static char * const SPA_TYPE_INFO_MEDIA_TYPE_BASE;
static char * const SPA_TYPE_INFO_MediaSubtype;
static char * const SPA_TYPE_INFO_MEDIA_SUBTYPE_BASE;
static char * const SPA_TYPE_INFO_FormatAudio;
static char * const SPA_TYPE_INFO_FORMAT_AUDIO_BASE;
static char * const SPA_TYPE_INFO_FormatVideo;
static char * const SPA_TYPE_INFO_FORMAT_VIDEO_BASE;
static char * const SPA_TYPE_INFO_FORMAT_VIDEO_H264;
static char * const SPA_TYPE_INFO_FORMAT_VIDEO_H264_BASE;
static char * const SPA_TYPE_INFO_PARAM_Buffers;
static char * const SPA_TYPE_INFO_PARAM_BUFFERS_BASE;
static char * const SPA_TYPE_INFO_PARAM_BlockInfo;
static char * const SPA_TYPE_INFO_PARAM_BLOCK_INFO_BASE;
static char * const SPA_TYPE_INFO_ParamAvailability;
static char * const SPA_TYPE_INFO_PARAM_AVAILABILITY_BASE;
static char * const SPA_TYPE_INFO_PARAM_Profile;
static char * const SPA_TYPE_INFO_PARAM_PROFILE_BASE;
static char * const SPA_TYPE_INFO_ParamPortConfigMode;
static char * const SPA_TYPE_INFO_PARAM_PORT_CONFIG_MODE_BASE;
static char * const SPA_TYPE_INFO_PARAM_PortConfig;
static char * const SPA_TYPE_INFO_PARAM_PORT_CONFIG_BASE;
static char * const SPA_TYPE_INFO_PARAM_Route;
static char * const SPA_TYPE_INFO_PARAM_ROUTE_BASE;
static char * const SPA_TYPE_INFO_Profiler;
static char * const SPA_TYPE_INFO_PROFILER_BASE;
static char * const SPA_TYPE_INFO_PARAM_Latency;
static char * const SPA_TYPE_INFO_PARAM_LATENCY_BASE;
static char * const SPA_TYPE_INFO_PARAM_ProcessLatency;
static char * const SPA_TYPE_INFO_PARAM_PROCESS_LATENCY_BASE;

static const struct spa_type_info spa_type_param[...];
static const struct spa_type_info spa_type_prop_float_array[...];
static const struct spa_type_info spa_type_prop_channel_map[...];
static const struct spa_type_info spa_type_prop_iec958_codec[...];
static const struct spa_type_info spa_type_props[...];
static const struct spa_type_info spa_type_prop_info[...];
static const struct spa_type_info spa_type_param_meta[...];
static const struct spa_type_info spa_type_param_io[...];
static const struct spa_type_info spa_type_media_type[...];
static const struct spa_type_info spa_type_media_subtype[...];
static const struct spa_type_info spa_type_format[...];
static const struct spa_type_info spa_type_param_buffers[...];
static const struct spa_type_info spa_type_param_availability[...];
static const struct spa_type_info spa_type_param_profile[...];
static const struct spa_type_info spa_type_param_port_config_mode[...];
static const struct spa_type_info spa_type_param_port_config[...];
static const struct spa_type_info spa_type_param_route[...];
static const struct spa_type_info spa_type_profiler[...];
static const struct spa_type_info spa_type_param_latency[...];
static const struct spa_type_info spa_type_param_process_latency[...];
"""


# XXX: SPA_POD_BUILDER_INIT(buffer, size)
# XXX: SPA_POD_INIT(size, type)
# XXX: SPA_POD_INIT_*(...)
# XXX: SPA_POD_BUILDER_COLLECT(builder, type, args)
# NOTE: spa_pod_builder_addv not implemented, va_list argument.
# XXX: spa_pod_builder_add_(object|struct|sequence)(...)
SOURCE += """
#include <spa/pod/builder.h>
"""
CDEF += """
struct spa_pod_builder_state {
    uint32_t offset;
    uint32_t flags;
    struct spa_pod_frame *frame;
};
struct spa_pod_builder_callbacks {
    uint32_t version;
    int (*overflow) (void *data, uint32_t size);
};
struct spa_pod_builder {
    void *data;
    uint32_t size;
    uint32_t _padding;
    struct spa_pod_builder_state state;
    struct spa_callbacks callbacks;
};

static const int SPA_POD_BUILDER_FLAG_BODY;
static const int SPA_POD_BUILDER_FLAG_FIRST;
static const int SPA_VERSION_POD_BUILDER_CALLBACKS;

void spa_pod_builder_get_state(struct spa_pod_builder *builder, struct spa_pod_builder_state *state);
void spa_pod_builder_set_callbacks(struct spa_pod_builder *builder, const struct spa_pod_builder_callbacks *callbacks, void *data);
void spa_pod_builder_reset(struct spa_pod_builder *builder, struct spa_pod_builder_state *state);
void spa_pod_builder_init(struct spa_pod_builder *builder, void *data, uint32_t size);
struct spa_pod *spa_pod_builder_deref(struct spa_pod_builder *builder, uint32_t offset);
struct spa_pod *spa_pod_builder_frame(struct spa_pod_builder *builder, struct spa_pod_frame *frame);
void spa_pod_builder_push(struct spa_pod_builder *builder, struct spa_pod_frame *frame, const struct spa_pod *pod, uint32_t offset);
int spa_pod_builder_raw(struct spa_pod_builder *builder, const void *data, uint32_t size);
int spa_pod_builder_pad(struct spa_pod_builder *builder, uint32_t size);
int spa_pod_builder_raw_padded(struct spa_pod_builder *builder, const void *data, uint32_t size);
void *spa_pod_builder_pop(struct spa_pod_builder *builder, struct spa_pod_frame *frame);
int spa_pod_builder_primitive(struct spa_pod_builder *builder, const struct spa_pod *p);
int spa_pod_builder_none(struct spa_pod_builder *builder);
int spa_pod_builder_child(struct spa_pod_builder *builder, uint32_t size, uint32_t type);
int spa_pod_builder_bool(struct spa_pod_builder *builder, bool val);
int spa_pod_builder_id(struct spa_pod_builder *builder, uint32_t val);
int spa_pod_builder_int(struct spa_pod_builder *builder, int32_t val);
int spa_pod_builder_long(struct spa_pod_builder *builder, int64_t val);
int spa_pod_builder_float(struct spa_pod_builder *builder, float val);
int spa_pod_builder_double(struct spa_pod_builder *builder, double val);
int spa_pod_builder_write_string(struct spa_pod_builder *builder, const char *str, uint32_t len);
int spa_pod_builder_string_len(struct spa_pod_builder *builder, const char *str, uint32_t len);
int spa_pod_builder_string(struct spa_pod_builder *builder, const char *str);
int spa_pod_builder_bytes(struct spa_pod_builder *builder, const void *bytes, uint32_t len);
void *spa_pod_builder_reserve_bytes(struct spa_pod_builder *builder, uint32_t len);
int spa_pod_builder_pointer(struct spa_pod_builder *builder, uint32_t type, const void *val);
int spa_pod_builder_fd(struct spa_pod_builder *builder, int64_t fd);
int spa_pod_builder_rectangle(struct spa_pod_builder *builder, uint32_t width, uint32_t height);
int spa_pod_builder_fraction(struct spa_pod_builder *builder, uint32_t num, uint32_t denom);
int spa_pod_builder_push_array(struct spa_pod_builder *builder, struct spa_pod_frame *frame);
int spa_pod_builder_array(struct spa_pod_builder *builder, uint32_t child_size, uint32_t child_type, uint32_t n_elems, const void *elems);
int spa_pod_builder_push_choice(struct spa_pod_builder *builder, struct spa_pod_frame *frame, uint32_t type, uint32_t flags);
int spa_pod_builder_push_struct(struct spa_pod_builder *builder, struct spa_pod_frame *frame);
int spa_pod_builder_push_object(struct spa_pod_builder *builder, struct spa_pod_frame *frame, uint32_t type, uint32_t id);
int spa_pod_builder_prop(struct spa_pod_builder *builder, uint32_t key, uint32_t flags);
int spa_pod_builder_push_sequence(struct spa_pod_builder *builder, struct spa_pod_frame *frame, uint32_t unit);
uint32_t spa_pod_builder_control(struct spa_pod_builder *builder, uint32_t offset, uint32_t type);
uint32_t spa_choice_from_id(char id);
int spa_pod_builder_add(struct spa_pod_builder *builder, ...);
struct spa_pod *spa_pod_copy(const struct spa_pod *pod);
"""

# XXX: SPA_COMMAND_INIT_FULL(t, size, type, id, ...), SPA_COMMAND_INIT(type, id)
SOURCE += """
#include <spa/pod/command.h>
"""
CDEF += """
struct spa_command_body {
    struct spa_pod_object_body body;
};
struct spa_command {
    struct spa_pod pod;
    struct spa_command_body body;
};

uint32_t SPA_COMMAND_TYPE(struct spa_command *cmd);
uint32_t SPA_COMMAND_ID(struct spa_command *cmd, uint32_t type);
"""

SOURCE += """
#include <spa/pod/compare.h>
"""
CDEF += """
int spa_pod_compare_value(uint32_t type, const void *r1, const void *r2, uint32_t size);
int spa_pod_compare(const struct spa_pod *pod1, const struct spa_pod *pod2);
"""

# XXX: SPA_EVENT_INIT_FULL(t, size, type, id, ...), SPA_EVENT_INIT(type, id)
SOURCE += """
#include <spa/pod/event.h>
"""
CDEF += """
struct spa_event_body {
    struct spa_pod_object_body body;
};
struct spa_event {
    struct spa_pod pod;
    struct spa_event_body body;
};

uint32_t SPA_EVENT_TYPE(struct spa_event *ev);
uint32_t SPA_EVENT_ID(struct spa_event *ev, uint32_t type);
"""

SOURCE += """
#include <spa/pod/filter.h>
"""
CDEF += """
int spa_pod_choice_fix_default(struct spa_pod_choice *choice);
int spa_pod_filter_flags_value(struct spa_pod_builder *b, uint32_t type, const void *r1, const void *r2, uint32_t size);
int spa_pod_filter_prop(struct spa_pod_builder *b, const struct spa_pod_prop *p1, const struct spa_pod_prop *p2);
int spa_pod_filter_part(struct spa_pod_builder *b, const struct spa_pod *pod, uint32_t pod_size, const struct spa_pod *filter, uint32_t filter_size);
int spa_pod_filter(struct spa_pod_builder *b, struct spa_pod **result, const struct spa_pod *pod, const struct spa_pod *filter);
"""

# XXX: SPA_POD_ARRAY_BODY_FOREACH(body, _size, iter)
# XXX: SPA_POD_ARRAY_FOREACH(obj, iter)
# XXX: SPA_POD_CHOICE_BODY_FOREACH(body, _size, iter)
# XXX: SPA_POD_CHOICE_FOREACH(obj, iter)
# XXX: SPA_POD_FOREACH(pod, size, iter)
# XXX: SPA_POD_STRUCT_FOREACH(obj, iter)
# XXX: SPA_POD_OBJECT_BODY_FOREACH(body, size, iter)
# XXX: SPA_POD_OBJECT_FOREACH(obj, iter)
# XXX: SPA_POD_SEQUENCE_BODY_FOREACH(body, size, iter)
# XXX: SPA_POD_SEQUENCE_FOREACH(seq, iter)
# NOTE: off_t from <sys/types.h>
SOURCE += """
#include <spa/pod/iter.h>
"""
CDEF += """
typedef ... off_t;

struct spa_pod_frame {
    struct spa_pod pod;
    struct spa_pod_frame *parent;
    uint32_t offset;
    uint32_t flags;
};

bool spa_pod_is_inside(const void *pod, uint32_t size, const void *iter);
void *spa_pod_next(const void *iter);
struct spa_pod_prop *spa_pod_prop_first(const struct spa_pod_object_body *body);
bool spa_pod_prop_is_inside(const struct spa_pod_object_body *body, uint32_t size, const struct spa_pod_prop *iter);
struct spa_pod_prop *spa_pod_prop_next(const struct spa_pod_prop *iter);
struct spa_pod_control *spa_pod_control_first(const struct spa_pod_sequence_body *body);
bool spa_pod_control_is_inside(const struct spa_pod_sequence_body *body, uint32_t size, const struct spa_pod_control *iter);
struct spa_pod_control *spa_pod_control_next(const struct spa_pod_control *iter);
void *spa_pod_from_data(void *data, size_t maxsize, off_t offset, size_t size);
int spa_pod_is_none(const struct spa_pod *pod);
int spa_pod_is_bool(const struct spa_pod *pod);
int spa_pod_get_bool(const struct spa_pod *pod, bool *value);
int spa_pod_is_id(const struct spa_pod *pod);
int spa_pod_get_id(const struct spa_pod *pod, uint32_t *value);
int spa_pod_is_int(const struct spa_pod *pod);
int spa_pod_get_int(const struct spa_pod *pod, int32_t *value);
int spa_pod_is_long(const struct spa_pod *pod);
int spa_pod_get_long(const struct spa_pod *pod, int64_t *value);
int spa_pod_is_float(const struct spa_pod *pod);
int spa_pod_get_float(const struct spa_pod *pod, float *value);
int spa_pod_is_double(const struct spa_pod *pod);
int spa_pod_get_double(const struct spa_pod *pod, double *value);
int spa_pod_is_string(const struct spa_pod *pod);
int spa_pod_get_string(const struct spa_pod *pod, const char **value);
int spa_pod_copy_string(const struct spa_pod *pod, size_t maxlen, char *dest);
int spa_pod_is_bytes(const struct spa_pod *pod);
int spa_pod_get_bytes(const struct spa_pod *pod, const void **value, uint32_t *len);
int spa_pod_is_pointer(const struct spa_pod *pod);
int spa_pod_get_pointer(const struct spa_pod *pod, uint32_t *type, const void **value);
int spa_pod_is_fd(const struct spa_pod *pod);
int spa_pod_get_fd(const struct spa_pod *pod, int64_t *value);
int spa_pod_is_rectangle(const struct spa_pod *pod);
int spa_pod_get_rectangle(const struct spa_pod *pod, struct spa_rectangle *value);
int spa_pod_is_fraction(const struct spa_pod *pod);
int spa_pod_get_fraction(const struct spa_pod *pod, struct spa_fraction *value);
int spa_pod_is_bitmap(const struct spa_pod *pod);
int spa_pod_is_array(const struct spa_pod *pod);
void *spa_pod_get_array(const struct spa_pod *pod, uint32_t *n_values);
uint32_t spa_pod_copy_array(const struct spa_pod *pod, uint32_t type, void *values, uint32_t max_values);
int spa_pod_is_choice(const struct spa_pod *pod);
struct spa_pod *spa_pod_get_values(const struct spa_pod *pod, uint32_t *n_vals, uint32_t *choice);
int spa_pod_is_struct(const struct spa_pod *pod);
int spa_pod_is_object(const struct spa_pod *pod);
bool spa_pod_is_object_type(const struct spa_pod *pod, uint32_t type);
bool spa_pod_is_object_id(const struct spa_pod *pod, uint32_t id);
int spa_pod_is_sequence(const struct spa_pod *pod);
const struct spa_pod_prop *spa_pod_object_find_prop(const struct spa_pod_object *pod, const struct spa_pod_prop *start, uint32_t key);
const struct spa_pod_prop *spa_pod_find_prop(const struct spa_pod *pod, const struct spa_pod_prop *start, uint32_t key);
int spa_pod_object_fixate(struct spa_pod_object *pod);
int spa_pod_fixate(struct spa_pod *pod);
"""

# XXX: SPA_POD_PARSER_INIT(buffer, size)
# XXX: SPA_POD_PARSER_COLLECT(pod, _type, args)
# XXX: SPA_POD_PARSER_SKIP(_type, args)
# XXX: SPA_POD_OPT_*(val)
# XXX: spa_pod_parse(r_get_(object|struct)|_(object|struct))(...)
# NOTE: spa_pod_parser_getv not implemented, va_list argument.
SOURCE += """
#include <spa/pod/parser.h>
"""
CDEF += """
struct spa_pod_parser_state {
    uint32_t offset;
    uint32_t flags;
    struct spa_pod_frame *frame;
};
struct spa_pod_parser {
    const void *data;
    uint32_t size;
    uint32_t _padding;
    struct spa_pod_parser_state state;
};

void spa_pod_parser_init(struct spa_pod_parser *parser, const void *data, uint32_t size);
void spa_pod_parser_pod(struct spa_pod_parser *parser, const struct spa_pod *pod);
void spa_pod_parser_get_state(struct spa_pod_parser *parser, struct spa_pod_parser_state *state);
void spa_pod_parser_reset(struct spa_pod_parser *parser, struct spa_pod_parser_state *state);
struct spa_pod *spa_pod_parser_deref(struct spa_pod_parser *parser, uint32_t offset, uint32_t size);
struct spa_pod *spa_pod_parser_frame(struct spa_pod_parser *parser, struct spa_pod_frame *frame);
void spa_pod_parser_push(struct spa_pod_parser *parser, struct spa_pod_frame *frame, const struct spa_pod *pod, uint32_t offset);
struct spa_pod *spa_pod_parser_current(struct spa_pod_parser *parser);
void spa_pod_parser_advance(struct spa_pod_parser *parser, const struct spa_pod *pod);
struct spa_pod *spa_pod_parser_next(struct spa_pod_parser *parser);
int spa_pod_parser_pop(struct spa_pod_parser *parser, struct spa_pod_frame *frame);
int spa_pod_parser_get_bool(struct spa_pod_parser *parser, bool *value);
int spa_pod_parser_get_id(struct spa_pod_parser *parser, uint32_t *value);
int spa_pod_parser_get_int(struct spa_pod_parser *parser, int32_t *value);
int spa_pod_parser_get_long(struct spa_pod_parser *parser, int64_t *value);
int spa_pod_parser_get_float(struct spa_pod_parser *parser, float *value);
int spa_pod_parser_get_double(struct spa_pod_parser *parser, double *value);
int spa_pod_parser_get_string(struct spa_pod_parser *parser, const char **value);
int spa_pod_parser_get_bytes(struct spa_pod_parser *parser, const void **value, uint32_t *len);
int spa_pod_parser_get_pointer(struct spa_pod_parser *parser, uint32_t *type, const void **value);
int spa_pod_parser_get_fd(struct spa_pod_parser *parser, int64_t *value);
int spa_pod_parser_get_rectangle(struct spa_pod_parser *parser, struct spa_rectangle *value);
int spa_pod_parser_get_fraction(struct spa_pod_parser *parser, struct spa_fraction *value);
int spa_pod_parser_get_pod(struct spa_pod_parser *parser, struct spa_pod **value);
int spa_pod_parser_push_struct(struct spa_pod_parser *parser, struct spa_pod_frame *frame);
int spa_pod_parser_push_object(struct spa_pod_parser *parser, struct spa_pod_frame *frame, uint32_t type, uint32_t *id);
bool spa_pod_parser_can_collect(const struct spa_pod *pod, char type);
int spa_pod_parser_get(struct spa_pod_parser *parser, ...);
"""

# XXX: SPA_POD_CONTENTS_SIZE(type, pod), SPA_POD_CONTENTS(type, pod), SPA_POD_CONTENTS_CONST(type, pod), SPA_POD_VALUE(type, pod)
SOURCE += """
#include <spa/pod/pod.h>
"""
CDEF += """
struct spa_pod {
    uint32_t size;
    uint32_t type;
};
struct spa_pod_bool {
    struct spa_pod pod;
    int32_t value;
    int32_t _padding;
};
struct spa_pod_id {
    struct spa_pod pod;
    uint32_t value;
    int32_t _padding;
};
struct spa_pod_int {
    struct spa_pod pod;
    int32_t value;
    int32_t _padding;
};
struct spa_pod_long {
    struct spa_pod pod;
    int64_t value;
};
struct spa_pod_float {
    struct spa_pod pod;
    float value;
    int32_t _padding;
};
struct spa_pod_double {
    struct spa_pod pod;
    double value;
};
struct spa_pod_string {
    struct spa_pod pod;
};
struct spa_pod_bytes {
    struct spa_pod pod;
};
struct spa_pod_rectangle {
    struct spa_pod pod;
    struct spa_rectangle value;
};
struct spa_pod_fraction {
    struct spa_pod pod;
    struct spa_fraction value;
};
struct spa_pod_bitmap {
    struct spa_pod pod;
};
struct spa_pod_array_body {
    struct spa_pod child;
};
struct spa_pod_array {
    struct spa_pod pod;
    struct spa_pod_array_body body;
};
enum spa_choice_type {
    SPA_CHOICE_None,
    SPA_CHOICE_Range,
    SPA_CHOICE_Step,
    SPA_CHOICE_Enum,
    SPA_CHOICE_Flags,
};
struct spa_pod_choice_body {
    uint32_t type;
    uint32_t flags;
    struct spa_pod child;
};
struct spa_pod_choice {
    struct spa_pod pod;
    struct spa_pod_choice_body body;
};
struct spa_pod_struct {
    struct spa_pod pod;
};
struct spa_pod_object_body {
    uint32_t type;
    uint32_t id;
};
struct spa_pod_object {
    struct spa_pod pod;
    struct spa_pod_object_body body;
};
struct spa_pod_pointer_body {
    uint32_t type;
    uint32_t _padding;
    const void *value;
};
struct spa_pod_pointer {
    struct spa_pod pod;
    struct spa_pod_pointer_body body;
};
struct spa_pod_fd {
    struct spa_pod pod;
    int64_t value;
};
struct spa_pod_prop {
    uint32_t key;
    uint32_t flags;
    struct spa_pod value;
};
struct spa_pod_control {
    uint32_t offset;
    uint32_t type;
    struct spa_pod value;
};
struct spa_pod_sequence_body {
    uint32_t unit;
    uint32_t pad;
};
struct spa_pod_sequence {
    struct spa_pod pod;
    struct spa_pod_sequence_body body;
};

static const int SPA_POD_PROP_FLAG_READONLY;
static const int SPA_POD_PROP_FLAG_HARDWARE;
static const int SPA_POD_PROP_FLAG_HINT_DICT;
static const int SPA_POD_PROP_FLAG_MANDATORY;
static const int SPA_POD_PROP_FLAG_DONT_FIXATE;
uint32_t SPA_POD_BODY_SIZE(void *pod);
uint32_t SPA_POD_TYPE(void *pod);
uint32_t SPA_POD_SIZE(void *pod);
void *SPA_POD_BODY(void *pod);
const void *SPA_POD_BODY_CONST(void *pod);
struct spa_pod *SPA_POD_ARRAY_CHILD(struct spa_pod_array *arr);
uint32_t SPA_POD_ARRAY_VALUE_TYPE(struct spa_pod_array *arr);
uint32_t SPA_POD_ARRAY_VALUE_SIZE(struct spa_pod_array *arr);
uint32_t SPA_POD_ARRAY_N_VALUES(struct spa_pod_array *arr);
void *SPA_POD_ARRAY_VALUES(struct spa_pod_array *arr);
struct spa_pod *SPA_POD_CHOICE_CHILD(struct spa_pod_choice *choice);
uint32_t SPA_POD_CHOICE_TYPE(struct spa_pod_choice *choice);
uint32_t SPA_POD_CHOICE_FLAGS(struct spa_pod_choice *choice);
uint32_t SPA_POD_CHOICE_VALUE_TYPE(struct spa_pod_choice *choice);
uint32_t SPA_POD_CHOICE_VALUE_SIZE(struct spa_pod_choice *choice);
uint32_t SPA_POD_CHOICE_N_VALUES(struct spa_pod_choice *choice);
void *SPA_POD_CHOICE_VALUES(struct spa_pod_choice *choice);
uint32_t SPA_POD_OBJECT_TYPE(struct spa_pod_object *obj);
uint32_t SPA_POD_OBJECT_ID(struct spa_pod_object *obj);
uint32_t SPA_POD_PROP_SIZE(struct spa_pod_prop *prop);
uint32_t SPA_POD_CONTROL_SIZE(struct spa_pod_control *ev);
"""

# XXX: macros
SOURCE += """
#include <spa/pod/vararg.h>
"""
CDEF += """
"""


SOURCE += """
#include <spa/support/cpu.h>
"""
CDEF += """
struct spa_cpu {
    struct spa_interface iface;
};
struct spa_cpu_methods {
    uint32_t version;
    uint32_t (*get_flags) (void *object);
    int (*force_flags) (void *object, uint32_t flags);
    uint32_t (*get_count) (void *object);
    uint32_t (*get_max_align) (void *object);
    uint32_t (*get_vm_type) (void *object);
};

static char * const SPA_TYPE_INTERFACE_CPU;
static const int SPA_VERSION_CPU;
static const int SPA_CPU_FLAG_MMX;
static const int SPA_CPU_FLAG_MMXEXT;
static const int SPA_CPU_FLAG_3DNOW;
static const int SPA_CPU_FLAG_SSE;
static const int SPA_CPU_FLAG_SSE2;
static const int SPA_CPU_FLAG_3DNOWEXT;
static const int SPA_CPU_FLAG_SSE3;
static const int SPA_CPU_FLAG_SSSE3;
static const int SPA_CPU_FLAG_SSE41;
static const int SPA_CPU_FLAG_SSE42;
static const int SPA_CPU_FLAG_AESNI;
static const int SPA_CPU_FLAG_AVX;
static const int SPA_CPU_FLAG_XOP;
static const int SPA_CPU_FLAG_FMA4;
static const int SPA_CPU_FLAG_CMOV;
static const int SPA_CPU_FLAG_AVX2;
static const int SPA_CPU_FLAG_FMA3;
static const int SPA_CPU_FLAG_BMI1;
static const int SPA_CPU_FLAG_BMI2;
static const int SPA_CPU_FLAG_AVX512;
static const int SPA_CPU_FLAG_SLOW_UNALIGNED;
static const int SPA_CPU_FLAG_ALTIVEC;
static const int SPA_CPU_FLAG_VSX;
static const int SPA_CPU_FLAG_POWER8;
static const int SPA_CPU_FLAG_ARMV5TE;
static const int SPA_CPU_FLAG_ARMV6;
static const int SPA_CPU_FLAG_ARMV6T2;
static const int SPA_CPU_FLAG_VFP;
static const int SPA_CPU_FLAG_VFPV3;
static const int SPA_CPU_FLAG_NEON;
static const int SPA_CPU_FLAG_ARMV8;
static const int SPA_CPU_FORCE_AUTODETECT;
static const int SPA_CPU_VM_NONE;
static const int SPA_CPU_VM_OTHER;
static const int SPA_CPU_VM_KVM;
static const int SPA_CPU_VM_QEMU;
static const int SPA_CPU_VM_BOCHS;
static const int SPA_CPU_VM_XEN;
static const int SPA_CPU_VM_UML;
static const int SPA_CPU_VM_VMWARE;
static const int SPA_CPU_VM_ORACLE;
static const int SPA_CPU_VM_MICROSOFT;
static const int SPA_CPU_VM_ZVM;
static const int SPA_CPU_VM_PARALLELS;
static const int SPA_CPU_VM_BHYVE;
static const int SPA_CPU_VM_QNX;
static const int SPA_CPU_VM_ACRN;
static const int SPA_CPU_VM_POWERVM;
static const int SPA_VERSION_CPU_METHODS;
static char * const SPA_KEY_CPU_FORCE;
static char * const SPA_KEY_CPU_VM_TYPE;
int spa_cpu_get_flags(struct spa_cpu *c);
int spa_cpu_force_flags(struct spa_cpu *c, uint32_t f);
int spa_cpu_get_count(struct spa_cpu *c);
int spa_cpu_get_max_align(struct spa_cpu *c);
int spa_cpu_get_vm_type(struct spa_cpu *c);
"""

SOURCE += """
#include <spa/support/dbus.h>
"""
CDEF += """
struct spa_dbus {
    struct spa_interface iface;
};
enum spa_dbus_type {
    SPA_DBUS_TYPE_SESSION,
    SPA_DBUS_TYPE_SYSTEM,
    SPA_DBUS_TYPE_STARTER,
};
struct spa_dbus_connection_events {
    uint32_t version;
    void (*destroy) (void *data);
    void (*disconnected) (void *data);
};
struct spa_dbus_connection {
    uint32_t version;
    void *(*get) (struct spa_dbus_connection *conn);
    void (*destroy) (struct spa_dbus_connection *conn);
    void (*add_listener) (struct spa_dbus_connection *conn, struct spa_hook *listener, const struct spa_dbus_connection_events *events, void *data);
};
struct spa_dbus_methods {
    uint32_t version;
    struct spa_dbus_connection * (*get_connection) (void *object, enum spa_dbus_type type);
};

static char * const SPA_TYPE_INTERFACE_DBus;
static const int SPA_VERSION_DBUS;
static const int SPA_DBUS_CONNECTION_EVENT_DESTROY;
static const int SPA_DBUS_CONNECTION_EVENT_DISCONNECTED;
static const int SPA_DBUS_CONNECTION_EVENT_NUM;
static const int SPA_VERSION_DBUS_CONNECTION_EVENTS;
static const int SPA_VERSION_DBUS_CONNECTION;
static const int SPA_VERSION_DBUS_METHODS;
void *spa_dbus_connection_get(struct spa_dbus_connection *c);
void spa_dbus_connection_destroy(struct spa_dbus_connection *c);
void spa_dbus_connection_add_listener(struct spa_dbus_connection *c, struct spa_hook *listener, const struct spa_dbus_connection_events *events, void *data);

struct spa_dbus_connection *spa_dbus_get_connection(struct spa_dbus *dbus, enum spa_dbus_type type);
"""

# XXX: SPA_FORMAT_ARG_FUNC
SOURCE += """
#include <spa/support/i18n.h>
"""
CDEF += """
struct spa_i18n {
    struct spa_interface iface;
};
struct spa_i18n_methods {
    uint32_t version;
    const char *(*text) (void *object, const char *msgid);
    const char *(*ntext) (void *object, const char *msgid, const char *msgid_plural, unsigned long int n);
};

static char * const SPA_TYPE_INTERFACE_I18N;
static const int SPA_VERSION_I18N;
static const int SPA_VERSION_I18N_METHODS;

static inline const char *spa_i18n_text(struct spa_i18n *i18n, const char *msgid);
static inline const char *spa_i18n_ntext(struct spa_i18n *i18n, const char *msgid, const char *msgid_plural, unsigned long int n);
"""

# NOTE: enum spa_log_level is actually defined in <spa/support/log.h>, but needs to be {}-declared on the first mention.
# XXX: SPA_PRINTF_FUNC
# NOTE: spa_log_impl_logv not implemented, va_list argument.
# XXX: SPA_LOG_IMPL_DEFINE(name), SPA_LOG_IMPL_INIT(name), SPA_LOG_IMPL(name)
SOURCE += """
#include <spa/support/log-impl.h>
"""
CDEF += """
enum spa_log_level {
    SPA_LOG_LEVEL_NONE,
    SPA_LOG_LEVEL_ERROR,
    SPA_LOG_LEVEL_WARN,
    SPA_LOG_LEVEL_INFO,
    SPA_LOG_LEVEL_DEBUG,
    SPA_LOG_LEVEL_TRACE,
};

void spa_log_impl_log(void *object, enum spa_log_level level, const char *file, int line, const char *func, const char *fmt, ...);
"""

# XXX: SPA_PRINTF_FUNC
# NOTE: logv not implemented, va_list argument.
# XXX: macros
SOURCE += """
#include <spa/support/log.h>
"""
CDEF += """
struct spa_log {
    struct spa_interface iface;
    enum spa_log_level level;
};
struct spa_log_methods {
    uint32_t version;
    void (*log) (void *object, enum spa_log_level level, const char *file, int line, const char *func, const char *fmt, ...);
    ...;
};

static char * const SPA_TYPE_INTERFACE_Log;
static const int SPA_VERSION_LOG;
static const int SPA_VERSION_LOG_METHODS;
static char * const SPA_KEY_LOG_LEVEL;
static char * const SPA_KEY_LOG_COLORS;
static char * const SPA_KEY_LOG_FILE;
static char * const SPA_KEY_LOG_TIMESTAMP;
static char * const SPA_KEY_LOG_LINE;
bool spa_log_level_enabled(struct spa_log *l, enum spa_log_level lev);
"""

SOURCE += """
#include <spa/support/loop.h>
"""
CDEF += """
struct spa_loop {
    struct spa_interface iface;
};
struct spa_loop_control {
    struct spa_interface iface;
};
struct spa_loop_utils {
    struct spa_interface iface;
};
typedef void (*spa_source_func_t) (struct spa_source *source);
struct spa_source {
    struct spa_loop *loop;
    spa_source_func_t func;
    void *data;
    int fd;
    uint32_t mask;
    uint32_t rmask;
};
typedef ... spa_invoke_func_t;
struct spa_loop_methods {
    uint32_t version;
    int (*add_source) (void *object, struct spa_source *source);
    int (*update_source) (void *object, struct spa_source *source);
    int (*remove_source) (void *object, struct spa_source *source);
    int (*invoke) (void *object, spa_invoke_func_t func, uint32_t seq, const void *data, size_t size, bool block, void *user_data);
};
struct spa_loop_control_hooks {
    uint32_t version;
    void (*before) (void *data);
    void (*after) (void *data);
};
struct spa_loop_control_methods {
    uint32_t version;
    int (*get_fd) (void *object);
    void (*add_hook) (void *object, struct spa_hook *hook, const struct spa_loop_control_hooks *hooks, void *data);
    void (*enter) (void *object);
    void (*leave) (void *object);
    int (*iterate) (void *object, int timeout);
};
typedef ... spa_source_io_func_t;
typedef ... spa_source_idle_func_t;
typedef ... spa_source_event_func_t;
typedef ... spa_source_timer_func_t;
typedef ... spa_source_signal_func_t;
struct spa_loop_utils_methods {
    uint32_t version;
    struct spa_source *(*add_io) (void *object, int fd, uint32_t mask, bool close, spa_source_io_func_t func, void *data);
    int (*update_io) (void *object, struct spa_source *source, uint32_t mask);
    struct spa_source *(*add_idle) (void *object, bool enabled, spa_source_idle_func_t func, void *data);
    int (*enable_idle) (void *object, struct spa_source *source, bool enabled);
    struct spa_source *(*add_event) (void *object, spa_source_event_func_t func, void *data);
    int (*signal_event) (void *object, struct spa_source *source);
    struct spa_source *(*add_timer) (void *object, spa_source_timer_func_t func, void *data);
    int (*update_timer) (void *object, struct spa_source *source, struct timespec *value, struct timespec *interval, bool absolute);
    struct spa_source *(*add_signal) (void *object, int signal_number, spa_source_signal_func_t func, void *data);
    void (*destroy_source) (void *object, struct spa_source *source);
};

static char * const SPA_TYPE_INTERFACE_Loop;
static char * const SPA_TYPE_INTERFACE_DataLoop;
static const int SPA_VERSION_LOOP;
static char * const SPA_TYPE_INTERFACE_LoopControl;
static const int SPA_VERSION_LOOP_CONTROL;
static char * const SPA_TYPE_INTERFACE_LoopUtils;
static const int SPA_VERSION_LOOP_UTILS;
static const int SPA_VERSION_LOOP_METHODS;
static const int SPA_VERSION_LOOP_CONTROL_HOOKS;
static const int SPA_VERSION_LOOP_CONTROL_METHODS;
static const int SPA_VERSION_LOOP_UTILS_METHODS;
int spa_loop_add_source(struct spa_loop *l, struct spa_source *source);
int spa_loop_update_source(struct spa_loop *l, struct spa_source *source);
int spa_loop_remove_source(struct spa_loop *l, struct spa_source *source);
int spa_loop_invoke(struct spa_loop *l, spa_invoke_func_t func, uint32_t seq, const void *data, size_t size, bool block, void *user_data);
void spa_loop_control_hook_before(struct spa_hook_list *l);
void spa_loop_control_hook_after(struct spa_hook_list *l);
int spa_loop_control_get_fd(struct spa_loop_control *l);
void spa_loop_control_add_hook(struct spa_loop_control *l, struct spa_hook *hook, const struct spa_loop_control_hooks *hooks, void *data);
void spa_loop_control_enter(struct spa_loop_control *l);
void spa_loop_control_leave(struct spa_loop_control *l);
int spa_loop_control_iterate(struct spa_loop_control *l, int timeout);
struct spa_source *spa_loop_utils_add_io(struct spa_loop_utils *l, int fd, uint32_t mask, bool close, spa_source_io_func_t func, void *data);
int spa_loop_utils_update_io(struct spa_loop_utils *l, struct spa_source *source, uint32_t mask);
struct spa_source *spa_loop_utils_add_idle(struct spa_loop_utils *l, bool enabled, spa_source_idle_func_t func, void *data);
int spa_loop_utils_enable_idle(struct spa_loop_utils *l, struct spa_source *source, bool enabled);
struct spa_source *spa_loop_utils_add_event(struct spa_loop_utils *l, spa_source_event_func_t func, void *data);
int spa_loop_utils_signal_event(struct spa_loop_utils *l, struct spa_source *source);
struct spa_source *spa_loop_utils_add_timer(struct spa_loop_utils *l, spa_source_timer_func_t func, void *data);
int spa_loop_utils_update_timer(struct spa_loop_utils *l, struct spa_source *source, struct timespec *value, struct timespec *interval, bool absolute);
struct spa_source *spa_loop_utils_add_signal(struct spa_loop_utils *l, int signal_number, spa_source_signal_func_t func, void *data);
void spa_loop_utils_destroy_source(struct spa_loop_utils *l, struct spa_source *source);

extern "Python" {
    void py_cb_spa_loop_control_hook_before(void *data);
    void py_cb_spa_loop_control_hook_after(void *data);
}
"""

# XXX: >0.3.34: spa/support/plugin-loader.h
#               987282b376173c429936ba2589a4fab9744f4bb9

# XXX: spa_system_ioctl
SOURCE += """
#include <spa/support/system.h>
"""
CDEF += """
struct spa_system {
    struct spa_interface iface;
};
struct spa_poll_event {
    uint32_t events;
    void *data;
};
struct spa_system_methods {
    uint32_t version;
    ssize_t (*read) (void *object, int fd, void *buf, size_t count);
    ssize_t (*write) (void *object, int fd, const void *buf, size_t count);
    int (*ioctl) (void *object, int fd, unsigned long request, ...);
    int (*close) (void *object, int fd);
    int (*clock_gettime) (void *object, int clockid, struct timespec *value);
    int (*clock_getres) (void *object, int clockid, struct timespec *res);
    int (*pollfd_create) (void *object, int flags);
    int (*pollfd_add) (void *object, int pfd, int fd, uint32_t events, void *data);
    int (*pollfd_mod) (void *object, int pfd, int fd, uint32_t events, void *data);
    int (*pollfd_del) (void *object, int pfd, int fd);
    int (*pollfd_wait) (void *object, int pfd, struct spa_poll_event *ev, int n_ev, int timeout);
    int (*timerfd_create) (void *object, int clockid, int flags);
    int (*timerfd_settime) (void *object, int fd, int flags, const struct itimerspec *new_value, struct itimerspec *old_value);
    int (*timerfd_gettime) (void *object, int fd, struct itimerspec *curr_value);
    int (*timerfd_read) (void *object, int fd, uint64_t *expirations);
    int (*eventfd_create) (void *object, int flags);
    int (*eventfd_write) (void *object, int fd, uint64_t count);
    int (*eventfd_read) (void *object, int fd, uint64_t *count);
    int (*signalfd_create) (void *object, int signal, int flags);
    int (*signalfd_read) (void *object, int fd, int *signal);
};

static char * const SPA_TYPE_INTERFACE_System;
static char * const SPA_TYPE_INTERFACE_DataSystem;
static const int SPA_VERSION_SYSTEM;
static const int SPA_IO_IN;
static const int SPA_IO_OUT;
static const int SPA_IO_ERR;
static const int SPA_IO_HUP;
static const int SPA_FD_CLOEXEC;
static const int SPA_FD_NONBLOCK;
static const int SPA_FD_EVENT_SEMAPHORE;
static const int SPA_FD_TIMER_ABSTIME;
static const int SPA_FD_TIMER_CANCEL_ON_SET;
static const int SPA_VERSION_SYSTEM_METHODS;
ssize_t spa_system_read(struct spa_system *s, int fd, void *buf, size_t count);
ssize_t spa_system_write(struct spa_system *s, int fd, const void *buf, size_t count);
int spa_system_close(struct spa_system *s, int fd);
int spa_system_clock_gettime(struct spa_system *s, int clockid, struct timespec *value);
int spa_system_clock_getres(struct spa_system *s, int clockid, struct timespec *res);
int spa_system_pollfd_create(struct spa_system *s, int flags);
int spa_system_pollfd_add(struct spa_system *s, int pfd, int fd, uint32_t events, void *data);
int spa_system_pollfd_mod(struct spa_system *s, int pfd, int fd, uint32_t events, void *data);
int spa_system_pollfd_del(struct spa_system *s, int pfd, int fd);
int spa_system_pollfd_wait(struct spa_system *s, int pfd, struct spa_poll_event *ev, int n_ev, int timeout);
int spa_system_timerfd_create(struct spa_system *s, int clockid, int flags);
int spa_system_timerfd_settime(struct spa_system *s, int fd, int flags, const struct itimerspec *new_value, struct itimerspec *old_value);
int spa_system_timerfd_gettime(struct spa_system *s, int fd, struct itimerspec *curr_value);
int spa_system_timerfd_read(struct spa_system *s, int fd, uint64_t *expirations);
int spa_system_eventfd_create(struct spa_system *s, int flags);
int spa_system_eventfd_write(struct spa_system *s, int fd, uint64_t count);
int spa_system_eventfd_read(struct spa_system *s, int fd, uint64_t *count);
int spa_system_signalfd_create(struct spa_system *s, int signal, int flags);
int spa_system_signalfd_read(struct spa_system *s, int fd, int *signal);
"""

SOURCE += """
#include <spa/support/thread.h>
"""
CDEF += """
struct spa_thread_utils {
    struct spa_interface iface;
};
struct spa_thread_utils_methods {
    uint32_t version;
    struct spa_thread * (*create) (void *data, const struct spa_dict *props, void *(*start)(void*), void *arg);
    int (*join)(void *data, struct spa_thread *thread, void **retval);
    int (*get_rt_range) (void *data, const struct spa_dict *props, int *min, int *max);
    int (*acquire_rt) (void *data, struct spa_thread *thread, int priority);
    int (*drop_rt) (void *data, struct spa_thread *thread);
};

static char * const SPA_TYPE_INFO_Thread;
static char * const SPA_TYPE_INTERFACE_ThreadUtils;
static const int SPA_VERSION_THREAD_UTILS;
static const int SPA_VERSION_THREAD_UTILS_METHODS;

struct spa_thread *spa_thread_utils_create(struct spa_thread_utils *o, const struct spa_dict *props, void *(*start_routine)(void*), void *arg);
int spa_thread_utils_join(struct spa_thread_utils *o, struct spa_thread *thread, void **retval);
int spa_thread_utils_get_rt_range(struct spa_thread_utils *o, const struct spa_dict *props, int *min, int *max);
int spa_thread_utils_acquire_rt(struct spa_thread_utils *o, struct spa_thread *thread, int priority);
int spa_thread_utils_drop_rt(struct spa_thread_utils *o, struct spa_thread *thread);
"""


SOURCE += """
#include <spa/utils/ansi.h>
"""
CDEF += """
static char * const SPA_ANSI_RESET;
static char * const SPA_ANSI_BOLD;
static char * const SPA_ANSI_ITALIC;
static char * const SPA_ANSI_UNDERLINE;
static char * const SPA_ANSI_BLACK;
static char * const SPA_ANSI_RED;
static char * const SPA_ANSI_GREEN;
static char * const SPA_ANSI_YELLOW;
static char * const SPA_ANSI_BLUE;
static char * const SPA_ANSI_MAGENTA;
static char * const SPA_ANSI_CYAN;
static char * const SPA_ANSI_WHITE;
static char * const SPA_ANSI_BRIGHT_BLACK;
static char * const SPA_ANSI_BRIGHT_RED;
static char * const SPA_ANSI_BRIGHT_GREEN;
static char * const SPA_ANSI_BRIGHT_YELLOW;
static char * const SPA_ANSI_BRIGHT_BLUE;
static char * const SPA_ANSI_BRIGHT_MAGENTA;
static char * const SPA_ANSI_BRIGHT_CYAN;
static char * const SPA_ANSI_BRIGHT_WHITE;
static char * const SPA_ANSI_BOLD_BLACK;
static char * const SPA_ANSI_BOLD_RED;
static char * const SPA_ANSI_BOLD_GREEN;
static char * const SPA_ANSI_BOLD_YELLOW;
static char * const SPA_ANSI_BOLD_BLUE;
static char * const SPA_ANSI_BOLD_MAGENTA;
static char * const SPA_ANSI_BOLD_CYAN;
static char * const SPA_ANSI_BOLD_WHITE;
static char * const SPA_ANSI_DARK_BLACK;
static char * const SPA_ANSI_DARK_RED;
static char * const SPA_ANSI_DARK_GREEN;
static char * const SPA_ANSI_DARK_YELLOW;
static char * const SPA_ANSI_DARK_BLUE;
static char * const SPA_ANSI_DARK_MAGENTA;
static char * const SPA_ANSI_DARK_CYAN;
static char * const SPA_ANSI_DARK_WHITE;
static char * const SPA_ANSI_BG_BLACK;
static char * const SPA_ANSI_BG_RED;
static char * const SPA_ANSI_BG_GREEN;
static char * const SPA_ANSI_BG_YELLOW;
static char * const SPA_ANSI_BG_BLUE;
static char * const SPA_ANSI_BG_MAGENTA;
static char * const SPA_ANSI_BG_CYAN;
static char * const SPA_ANSI_BG_WHITE;
static char * const SPA_ANSI_BG_BRIGHT_BLACK;
static char * const SPA_ANSI_BG_BRIGHT_RED;
static char * const SPA_ANSI_BG_BRIGHT_GREEN;
static char * const SPA_ANSI_BG_BRIGHT_YELLOW;
static char * const SPA_ANSI_BG_BRIGHT_BLUE;
static char * const SPA_ANSI_BG_BRIGHT_MAGENTA;
static char * const SPA_ANSI_BG_BRIGHT_CYAN;
static char * const SPA_ANSI_BG_BRIGHT_WHITE;

"""

# XXX: SPA_FALLTHROUGH
# XXX: do SPA_FLAG_(SET|CLEAR|UPDATE) work??
# XXX: SPA_RECTANGLE(width, height), SPA_POINT(x, y), SPA_REGION(x, y, width, height), SPA_FRACTION(num, denom)
# XXX: SPA_N_ELEMENTS(arr)
# XXX: SPA_FOR_EACH_ELEMENTS(arr, ptr)
# XXX: SPA_MIN(a, b), SPA_MAX(a, b), SPA_CLAMP(v, low, high), SPA_SWAP(a, b), SPA_TYPECHECK(type, x)
# XXX: SPA_PTROFF(ptr_, offset_, type_), SPA_PTROFF_ALIGN(ptr_, offset_, alignment_, type_), SPA_CONTAINER_OF(p, t, m)
# XXX: SPA_MEMBER(b, o, t), SPA_MEMBER_ALIGN(b, o, a, t) (deprecated)
# XXX: SPA_PRINTF_FUNC(fmt, arg1), SPA_FORMAT_ARG_FUNC(arg1), SPA_ALIGNED(align), SPA_DEPRECATED, SPA_EXPORT, SPA_SENTINEL, SPA_UNUSED, SPA_NORETURN
# XXX: SPA_RESTRICT
# XXX: SPA_PTR_ALIGN
# XXX: SPA_LIKELY
# XXX: SPA_STRINGIFY_1(...), SPA_STRINGIFY(...)
# XXX: spa_return_if_fail(expr), spa_return_val_if_fail(expr, val), spa_assert_se(expr), spa_nop(), spa_assert(expr), spa_assert_not_reached()
# XXX: spa_zero(x)
# XXX: spa_aprintf(_fmt, ...)
SOURCE += """
#include <spa/utils/defs.h>
"""
CDEF += """
struct spa_rectangle {
    uint32_t width;
    uint32_t height;
};
struct spa_point {
    int32_t x;
    int32_t y;
};
struct spa_region {
    struct spa_point position;
    struct spa_rectangle size;
};
struct spa_fraction {
    uint32_t num;
    uint32_t denom;
};

static const int64_t SPA_TIME_INVALID;
static const unsigned int SPA_IDX_INVALID;
static const uint32_t SPA_ID_INVALID;
static const long long SPA_NSEC_PER_SEC;
static const long long SPA_NSEC_PER_MSEC;
static const long long SPA_NSEC_PER_USEC;
static const long long SPA_USEC_PER_SEC;
static const long long SPA_USEC_PER_MSEC;
static const long long SPA_MSEC_PER_SEC;
bool SPA_FLAG_MASK(uint32_t field, uint32_t mask, uint32_t flag);
bool SPA_FLAG_IS_SET(uint32_t field, uint32_t flag);
uint32_t SPA_FLAG_SET(uint32_t field, uint32_t flag);
uint32_t SPA_FLAG_CLEAR(uint32_t field, uint32_t flag);
uint32_t SPA_FLAG_UPDATE(uint32_t field, uint32_t flag, uint32_t val);
uint32_t SPA_DIRECTION_REVERSE(uint32_t d);
int16_t SPA_PTRDIFF(uint8_t *p1, uint8_t *p2);
int SPA_PTR_TO_INT(intptr_t p);
void *SPA_INT_TO_PTR(intptr_t u);
uint32_t SPA_PTR_TO_UINT32(uintptr_t p);
void *SPA_UINT32_TO_PTR(uintptr_t u);
long long SPA_TIMESPEC_TO_NSEC(struct timespec *ts);
long long SPA_TIMESPEC_TO_USEC(struct timespec *ts);
long long SPA_TIMEVAL_TO_NSEC(struct timeval *tv);
long long SPA_TIMEVAL_TO_USEC(struct timeval *tv);
uint32_t SPA_ROUND_DOWN_N(uint32_t num, uint32_t align);
uint32_t SPA_ROUND_UP_N(uint32_t num, uint32_t align);
intptr_t SPA_PTR_ALIGNMENT(intptr_t p, intptr_t align);
bool SPA_IS_ALIGNED(intptr_t p, intptr_t align);
void *spa_memzero(void *x, size_t l);
void *spa_memcpy(void *d, const void *s, size_t n);
void *spa_memmove(void *d, const void *s, size_t n);
"""

# XXX: SPA_DICT_ITEM_INIT(key, value), SPA_DICT_INIT(items, n_items), SPA_DICT_INIT_ARRAY(items)
# XXX: spa_dict_for_each(item, dict)
SOURCE += """
#include <spa/utils/dict.h>
"""
CDEF += """
struct spa_dict_item {
    const char *key;
    const char *value;
};
struct spa_dict {
    uint32_t flags;
    uint32_t n_items;
    const struct spa_dict_item *items;
};

static const int SPA_DICT_FLAG_SORTED;

int spa_dict_item_compare(const void *i1, const void *i2);
void spa_dict_qsort(struct spa_dict *dict);
const struct spa_dict_item *spa_dict_lookup_item(const struct spa_dict *dict, const char *key);
const char *spa_dict_lookup(const struct spa_dict *dict, const char *key);
"""

# XXX: SPA_CALLBACK_CHECK(c, m, v)
# XXX: SPA_CALLBACKS_INIT(_funcs, _data), SPA_INTERFACE_INIT(_type, _version, _funcs, _data)
# XXX: spa_callbacks_call(_res), spa_interface_call(_res)
# XXX: spa_hook_list_(call_simple|do_call|call|call_once_start)
SOURCE += """
#include <spa/utils/hook.h>
"""
CDEF += """
struct spa_callbacks {
    const void *funcs;
    void *data;
};
struct spa_interface {
    const char *type;
    uint32_t version;
    struct spa_callbacks cb;
};
struct spa_hook_list {
    struct spa_list list;
};
struct spa_hook {
    struct spa_list link;
    struct spa_callbacks cb;
    void (*removed) (struct spa_hook *hook);
    void *priv;
};

void spa_hook_list_init(struct spa_hook_list *list);
bool spa_hook_list_is_empty(struct spa_hook_list *list);
void spa_hook_list_append(struct spa_hook_list *list, struct spa_hook *hook, const void *funcs, void *data);
void spa_hook_list_prepend(struct spa_hook_list *list, struct spa_hook *hook, const void *funcs, void *data);
void spa_hook_remove(struct spa_hook *hook);
void spa_hook_list_clean(struct spa_hook_list *list);
void spa_hook_list_isolate(struct spa_hook_list *list, struct spa_hook_list *save, struct spa_hook *hook, const void *funcs, void *data);
void spa_hook_list_join(struct spa_hook_list *list, struct spa_hook_list *save);
"""

# XXX: SPA_JSON_INIT(data, size)
# XXX: SPA_JSON_ENTER(iter)
# XXX: SPA_JSON_SAVE(iter)
SOURCE += """
#include <spa/utils/json.h>
"""
CDEF += """
struct spa_json {
    const char *cur;
    const char *end;
    struct spa_json *parent;
    uint32_t state;
    uint32_t depth;
};

void spa_json_init(struct spa_json * iter, const char *data, size_t size);
void spa_json_enter(struct spa_json * iter, struct spa_json * sub);
int spa_json_next(struct spa_json * iter, const char **value);
int spa_json_enter_container(struct spa_json *iter, struct spa_json *sub, char type);
int spa_json_is_container(const char *val, int len);
int spa_json_container_len(struct spa_json *iter, const char *value, int len);
int spa_json_is_object(const char *val, int len);
int spa_json_enter_object(struct spa_json *iter, struct spa_json *sub);
bool spa_json_is_array(const char *val, int len);
int spa_json_enter_array(struct spa_json *iter, struct spa_json *sub);
bool spa_json_is_null(const char *val, int len);
int spa_json_parse_float(const char *val, int len, float *result);
bool spa_json_is_float(const char *val, int len);
int spa_json_get_float(struct spa_json *iter, float *res);
int spa_json_parse_int(const char *val, int len, int *result);
bool spa_json_is_int(const char *val, int len);
int spa_json_get_int(struct spa_json *iter, int *res);
bool spa_json_is_true(const char *val, int len);
bool spa_json_is_false(const char *val, int len);
bool spa_json_is_bool(const char *val, int len);
int spa_json_parse_bool(const char *val, int len, bool *result);
int spa_json_get_bool(struct spa_json *iter, bool *res);
bool spa_json_is_string(const char *val, int len);
int spa_json_parse_string(const char *val, int len, char *result);
int spa_json_get_string(struct spa_json *iter, char *res, int maxlen);
int spa_json_encode_string(char *str, int size, const char *val);
"""

SOURCE += """
#include <spa/utils/keys.h>
"""
CDEF += """
static char * const SPA_KEY_OBJECT_PATH;
static char * const SPA_KEY_MEDIA_CLASS;
static char * const SPA_KEY_MEDIA_ROLE;
static char * const SPA_KEY_API_UDEV;
static char * const SPA_KEY_API_UDEV_MATCH;
static char * const SPA_KEY_API_ALSA;
static char * const SPA_KEY_API_ALSA_PATH;
static char * const SPA_KEY_API_ALSA_CARD;
static char * const SPA_KEY_API_ALSA_USE_UCM;
static char * const SPA_KEY_API_ALSA_IGNORE_DB;
static char * const SPA_KEY_API_ALSA_OPEN_UCM;
static char * const SPA_KEY_API_ALSA_CARD_ID;
static char * const SPA_KEY_API_ALSA_CARD_COMPONENTS;
static char * const SPA_KEY_API_ALSA_CARD_DRIVER;
static char * const SPA_KEY_API_ALSA_CARD_NAME;
static char * const SPA_KEY_API_ALSA_CARD_LONGNAME;
static char * const SPA_KEY_API_ALSA_CARD_MIXERNAME;
static char * const SPA_KEY_API_ALSA_PCM_ID;
static char * const SPA_KEY_API_ALSA_PCM_CARD;
static char * const SPA_KEY_API_ALSA_PCM_NAME;
static char * const SPA_KEY_API_ALSA_PCM_SUBNAME;
static char * const SPA_KEY_API_ALSA_PCM_STREAM;
static char * const SPA_KEY_API_ALSA_PCM_CLASS;
static char * const SPA_KEY_API_ALSA_PCM_DEVICE;
static char * const SPA_KEY_API_ALSA_PCM_SUBDEVICE;
static char * const SPA_KEY_API_ALSA_PCM_SUBCLASS;
static char * const SPA_KEY_API_ALSA_PCM_SYNC_ID;
static char * const SPA_KEY_API_V4L2;
static char * const SPA_KEY_API_V4L2_PATH;
static char * const SPA_KEY_API_LIBCAMERA;
static char * const SPA_KEY_API_LIBCAMERA_PATH;
static char * const SPA_KEY_API_LIBCAMERA_CAP_DRIVER;
static char * const SPA_KEY_API_LIBCAMERA_CAP_CARD;
static char * const SPA_KEY_API_LIBCAMERA_CAP_BUS_INFO;
static char * const SPA_KEY_API_LIBCAMERA_CAP_VERSION;
static char * const SPA_KEY_API_LIBCAMERA_CAP_CAPABILITIES;
static char * const SPA_KEY_API_LIBCAMERA_CAP_DEVICE_CAPS;
static char * const SPA_KEY_API_V4L2_CAP_DRIVER;
static char * const SPA_KEY_API_V4L2_CAP_CARD;
static char * const SPA_KEY_API_V4L2_CAP_BUS_INFO;
static char * const SPA_KEY_API_V4L2_CAP_VERSION;
static char * const SPA_KEY_API_V4L2_CAP_CAPABILITIES;
static char * const SPA_KEY_API_V4L2_CAP_DEVICE_CAPS;
static char * const SPA_KEY_API_BLUEZ5;
static char * const SPA_KEY_API_BLUEZ5_PATH;
static char * const SPA_KEY_API_BLUEZ5_DEVICE;
static char * const SPA_KEY_API_BLUEZ5_CONNECTION;
static char * const SPA_KEY_API_BLUEZ5_TRANSPORT;
static char * const SPA_KEY_API_BLUEZ5_PROFILE;
static char * const SPA_KEY_API_BLUEZ5_ADDRESS;
static char * const SPA_KEY_API_BLUEZ5_CODEC;
static char * const SPA_KEY_API_BLUEZ5_CLASS;
static char * const SPA_KEY_API_BLUEZ5_ICON;
static char * const SPA_KEY_API_JACK;
static char * const SPA_KEY_API_JACK_SERVER;
static char * const SPA_KEY_API_JACK_CLIENT;
"""

# XXX: SPA_LIST_INIT(list)
# XXX: spa_list_(first|last)(head, type, member), spa_list_is_end(pos, head, member), spa_list_(next|prev)(pos, member)
# XXX: spa_list_consume(pos, head, member), spa_list_for_each_next(pos, head, curr, member), spa_list_for_each_prev(pos, head, curr, member), spa_list_for_each(pos, head, member), spa_list_for_each_reverse(pos, head, member), spa_list_for_each_safe_next(pos, tmp, head, curr, member), spa_list_for_each_safe_prev(pos, tmp, head, curr, member), spa_list_for_each_safe(pos, tmp, head, member), spa_list_for_each_safe_reverse(pos, tmp, head, member), spa_list_cursor_start(cursor, head, member), spa_list_for_each_cursor(pos, cursor, head, member), spa_list_cursor_end(cursor, member)
SOURCE += """
#include <spa/utils/list.h>
"""
CDEF += """
struct spa_list {
    struct spa_list *next;
    struct spa_list *prev;
};

bool spa_list_is_empty(struct spa_list *l);
void spa_list_append(struct spa_list *list, struct spa_list *item);
void spa_list_prepend(struct spa_list *list, struct spa_list *item);

void spa_list_init(struct spa_list *list);
void spa_list_insert(struct spa_list *list, struct spa_list *elem);
void spa_list_insert_list(struct spa_list *list, struct spa_list *other);
void spa_list_remove(struct spa_list *elem);
"""

# XXX: >0.3.34: SPA_NAME_API_CODEC_BLUEZ5_A2DP
#               b5ad37c7ac6a2b8d66967f71751fc666812ec85f
SOURCE += """
#include <spa/utils/names.h>
"""
CDEF += """
static char * const SPA_NAME_SUPPORT_CPU;
static char * const SPA_NAME_SUPPORT_DBUS;
static char * const SPA_NAME_SUPPORT_LOG;
static char * const SPA_NAME_SUPPORT_LOOP;
static char * const SPA_NAME_SUPPORT_SYSTEM;
static char * const SPA_NAME_SUPPORT_NODE_DRIVER;
static char * const SPA_NAME_CONTROL_MIXER;
static char * const SPA_NAME_AUDIO_MIXER;
static char * const SPA_NAME_AUDIO_MIXER_DSP;
static char * const SPA_NAME_AUDIO_PROCESS_FORMAT;
static char * const SPA_NAME_AUDIO_PROCESS_CHANNELMIX;
static char * const SPA_NAME_AUDIO_PROCESS_RESAMPLE;
static char * const SPA_NAME_AUDIO_PROCESS_DEINTERLEAVE;
static char * const SPA_NAME_AUDIO_PROCESS_INTERLEAVE;
static char * const SPA_NAME_AUDIO_CONVERT;
static char * const SPA_NAME_AUDIO_ADAPT;
static char * const SPA_NAME_VIDEO_PROCESS_FORMAT;
static char * const SPA_NAME_VIDEO_PROCESS_SCALE;
static char * const SPA_NAME_VIDEO_CONVERT;
static char * const SPA_NAME_VIDEO_ADAPT;
static char * const SPA_NAME_API_ALSA_ENUM_UDEV;
static char * const SPA_NAME_API_ALSA_PCM_DEVICE;
static char * const SPA_NAME_API_ALSA_PCM_SOURCE;
static char * const SPA_NAME_API_ALSA_PCM_SINK;
static char * const SPA_NAME_API_ALSA_SEQ_DEVICE;
static char * const SPA_NAME_API_ALSA_SEQ_SOURCE;
static char * const SPA_NAME_API_ALSA_SEQ_SINK;
static char * const SPA_NAME_API_ALSA_SEQ_BRIDGE;
static char * const SPA_NAME_API_ALSA_ACP_DEVICE;
static char * const SPA_NAME_API_BLUEZ5_ENUM_DBUS;
static char * const SPA_NAME_API_BLUEZ5_DEVICE;
static char * const SPA_NAME_API_BLUEZ5_A2DP_SINK;
static char * const SPA_NAME_API_BLUEZ5_A2DP_SOURCE;
static char * const SPA_NAME_API_BLUEZ5_SCO_SINK;
static char * const SPA_NAME_API_BLUEZ5_SCO_SOURCE;
static char * const SPA_NAME_API_V4L2_ENUM_UDEV;
static char * const SPA_NAME_API_V4L2_DEVICE;
static char * const SPA_NAME_API_V4L2_SOURCE;
static char * const SPA_NAME_API_LIBCAMERA_ENUM_CLIENT;
static char * const SPA_NAME_API_LIBCAMERA_DEVICE;
static char * const SPA_NAME_API_LIBCAMERA_SOURCE;
static char * const SPA_NAME_API_JACK_DEVICE;
static char * const SPA_NAME_API_JACK_SOURCE;
static char * const SPA_NAME_API_JACK_SINK;
static char * const SPA_NAME_API_VULKAN_COMPUTE_SOURCE;
"""

SOURCE += """
#include <spa/utils/result.h>
"""
CDEF += """
static const uint32_t SPA_ASYNC_BIT;
static const uint32_t SPA_ASYNC_SEQ_MASK;
static const uint32_t SPA_ASYNC_MASK;
bool SPA_RESULT_IS_OK(uint32_t res);
bool SPA_RESULT_IS_ERROR(uint32_t res);
bool SPA_RESULT_IS_ASYNC(uint32_t res);
uint32_t SPA_RESULT_ASYNC_SEQ(uint32_t res);
uint32_t SPA_RESULT_RETURN_ASYNC(uint32_t seq);
char *spa_strerror(int err);
"""

# XXX: SPA_RINGBUFFER_INIT()
SOURCE += """
#include <spa/utils/ringbuffer.h>
"""
CDEF += """
struct spa_ringbuffer {
    uint32_t readindex;
    uint32_t writeindex;
};

static inline void spa_ringbuffer_init(struct spa_ringbuffer *rbuf);
static inline void spa_ringbuffer_set_avail(struct spa_ringbuffer *rbuf, uint32_t size);
static inline int32_t spa_ringbuffer_get_read_index(struct spa_ringbuffer *rbuf, uint32_t *index);
static inline void spa_ringbuffer_read_data(struct spa_ringbuffer *rbuf, const void *buffer, uint32_t size, uint32_t offset, void *data, uint32_t len);
static inline void spa_ringbuffer_read_update(struct spa_ringbuffer *rbuf, int32_t index);
static inline int32_t spa_ringbuffer_get_write_index(struct spa_ringbuffer *rbuf, uint32_t *index);
static inline void spa_ringbuffer_write_data(struct spa_ringbuffer *rbuf, void *buffer, uint32_t size, uint32_t offset, const void *data, uint32_t len);
static inline void spa_ringbuffer_write_update(struct spa_ringbuffer *rbuf, int32_t index);
"""

# NOTE: spa_vscnprintf not implemented, va_list argument.
# XXX: SPA_PRINTF_FUNC
SOURCE += """
#include <spa/utils/string.h>
"""
CDEF += """
bool spa_streq(const char *s1, const char *s2);
bool spa_strneq(const char *s1, const char *s2, size_t len);
bool spa_strstartswith(const char *s, const char *prefix);
bool spa_strendswith(const char *s, const char *suffix);
bool spa_atoi32(const char *str, int32_t *val, int base);
bool spa_atou32(const char *str, uint32_t *val, int base);
bool spa_atoi64(const char *str, int64_t *val, int base);
bool spa_atou64(const char *str, uint64_t *val, int base);
bool spa_atob(const char *str);
int spa_scnprintf(char *buffer, size_t size, const char *format, ...);
bool spa_atof(const char *str, float *val);
bool spa_atod(const char *str, double *val);
"""

# XXX: SPA_TYPE_ROOT
SOURCE += """
#include <spa/utils/type-info.h>
"""
CDEF += """
static char * const SPA_TYPE_INFO_Direction;
static char * const SPA_TYPE_INFO_DIRECTION_BASE;
static char * const SPA_TYPE_INFO_Choice;
static char * const SPA_TYPE_INFO_CHOICE_BASE;

bool spa_type_is_a(const char *type, const char *parent);

static const struct spa_type_info spa_type_direction[...];
static const struct spa_type_info spa_type_choice[...];
static const struct spa_type_info spa_types[...];
"""

SOURCE += """
#include <spa/utils/type.h>
"""
CDEF += """
enum {
    SPA_TYPE_START,
    SPA_TYPE_None,
    SPA_TYPE_Bool,
    SPA_TYPE_Id,
    SPA_TYPE_Int,
    SPA_TYPE_Long,
    SPA_TYPE_Float,
    SPA_TYPE_Double,
    SPA_TYPE_String,
    SPA_TYPE_Bytes,
    SPA_TYPE_Rectangle,
    SPA_TYPE_Fraction,
    SPA_TYPE_Bitmap,
    SPA_TYPE_Array,
    SPA_TYPE_Struct,
    SPA_TYPE_Object,
    SPA_TYPE_Sequence,
    SPA_TYPE_Pointer,
    SPA_TYPE_Fd,
    SPA_TYPE_Choice,
    SPA_TYPE_Pod,
    SPA_TYPE_POINTER_START,
    SPA_TYPE_POINTER_Buffer,
    SPA_TYPE_POINTER_Meta,
    SPA_TYPE_POINTER_Dict,
    SPA_TYPE_EVENT_START,
    SPA_TYPE_EVENT_Device,
    SPA_TYPE_EVENT_Node,
    SPA_TYPE_COMMAND_START,
    SPA_TYPE_COMMAND_Device,
    SPA_TYPE_COMMAND_Node,
    SPA_TYPE_OBJECT_START,
    SPA_TYPE_OBJECT_PropInfo,
    SPA_TYPE_OBJECT_Props,
    SPA_TYPE_OBJECT_Format,
    SPA_TYPE_OBJECT_ParamBuffers,
    SPA_TYPE_OBJECT_ParamMeta,
    SPA_TYPE_OBJECT_ParamIO,
    SPA_TYPE_OBJECT_ParamProfile,
    SPA_TYPE_OBJECT_ParamPortConfig,
    SPA_TYPE_OBJECT_ParamRoute,
    SPA_TYPE_OBJECT_Profiler,
    SPA_TYPE_OBJECT_ParamLatency,
    SPA_TYPE_OBJECT_ParamProcessLatency,
    SPA_TYPE_VENDOR_PipeWire,
    SPA_TYPE_VENDOR_Other,
};
struct spa_type_info {
};

static char * const SPA_TYPE_INFO_BASE;
static char * const SPA_TYPE_INFO_Flags;
static char * const SPA_TYPE_INFO_FLAGS_BASE;
static char * const SPA_TYPE_INFO_Enum;
static char * const SPA_TYPE_INFO_ENUM_BASE;
static char * const SPA_TYPE_INFO_Pod;
static char * const SPA_TYPE_INFO_POD_BASE;
static char * const SPA_TYPE_INFO_Struct;
static char * const SPA_TYPE_INFO_STRUCT_BASE;
static char * const SPA_TYPE_INFO_Object;
static char * const SPA_TYPE_INFO_OBJECT_BASE;
static char * const SPA_TYPE_INFO_Pointer;
static char * const SPA_TYPE_INFO_POINTER_BASE;
static char * const SPA_TYPE_INFO_Interface;
static char * const SPA_TYPE_INFO_INTERFACE_BASE;
static char * const SPA_TYPE_INFO_Event;
static char * const SPA_TYPE_INFO_EVENT_BASE;
static char * const SPA_TYPE_INFO_Command;
static char * const SPA_TYPE_INFO_COMMAND_BASE;
"""



ffi_builder = FFI()
ffi_builder.cdef(CDEF)
ffi_builder.set_source_pkgconfig(
    "pipewire._ffi_spa",
    # XXX: dynamic version?
    ["libspa-0.2"],
    SOURCE,
)


def build():
    ffi_builder.compile()


if __name__ == "__main__":
    build()
