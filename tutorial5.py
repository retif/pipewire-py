import pipewire



def make_stream_handle(extra_data):
    def cb_process():
        try:
            b = pipewire.lib.pw_stream_dequeue_buffer(extra_data["stream"])
            if b == pipewire.ffi.NULL:
                print("out of buffers")
                return

            buf = b.buffer
            if buf.datas[0].data == pipewire.ffi.NULL:
                return

            print(f"got a frame of size {buf.datas[0].chunk.size}")

            pipewire.lib.pw_stream_queue_buffer(extra_data["stream"], b)
        except KeyboardInterrupt:
            pipewire.lib.pw_main_loop_quit(extra_data["loop"])

    def cb_param_changed(id, param):
        try:
            if param == pipewire.ffi.NULL or id != pipewire.lib.SPA_PARAM_Format:
                return

            if pipewire.lib.spa_format_parse(param, pipewire.ffi.addressof(extra_data["format"], "media_type"), pipewire.ffi.addressof(extra_data["format"], "media_subtype")) < 0:
                return

            if extra_data["format"].media_type != pipewire.lib.SPA_MEDIA_TYPE_video or extra_data["format"].media_subtype != pipewire.lib.SPA_MEDIA_SUBTYPE_raw:
                return

            if pipewire.lib.spa_format_video_raw_parse(param, pipewire.ffi.addressof(extra_data["format"].info, "raw")) < 0:
                return

            print("got video format:");
            print(f"  format: {extra_data['format'].info.raw.format} ({pipewire.ffi.string(pipewire.lib.spa_debug_type_find_name(pipewire.lib.spa_type_video_format, extra_data['format'].info.raw.format)).decode()})")
            print(f"  size: {extra_data['format'].info.raw.size.width}x{extra_data['format'].info.raw.size.height}")
            print(f"  framerate: {extra_data['format'].info.raw.framerate.num}/{extra_data['format'].info.raw.framerate.denom}")
        except KeyboardInterrupt:
            pipewire.lib.pw_main_loop_quit(extra_data["loop"])

    return pipewire.ffi.new_handle({"process": cb_process, "param_changed": cb_param_changed})


def main():
    stream_events = pipewire.ffi.new("struct pw_stream_events *")
    stream_events.version = pipewire.lib.PW_VERSION_STREAM_EVENTS
    stream_events.process = pipewire.lib.py_cb_pw_stream_event_process
    stream_events.param_changed = pipewire.lib.py_cb_pw_stream_event_param_changed

    params = pipewire.ffi.new("struct spa_pod *[1]")

    buffer = pipewire.ffi.new("uint8_t[1024]")
    b = pipewire.ffi.new("struct spa_pod_builder *")
    b.data = buffer
    b.size = pipewire.ffi.sizeof(buffer)

    f = pipewire.ffi.new("struct spa_pod_frame *")

    r_def = pipewire.ffi.new("struct spa_rectangle *")
    r_def.width = 320
    r_def.height = 240
    r_min = pipewire.ffi.new("struct spa_rectangle *")
    r_min.width = 1
    r_min.height = 1
    r_max = pipewire.ffi.new("struct spa_rectangle *")
    r_max.width = 4096
    r_max.height = 4096

    f_def = pipewire.ffi.new("struct spa_fraction *")
    f_def.num = 25
    f_def.denom = 1
    f_min = pipewire.ffi.new("struct spa_fraction *")
    f_min.num = 0
    f_min.denom = 1
    f_max = pipewire.ffi.new("struct spa_fraction *")
    f_max.num = 1000
    f_max.denom = 1

    fmt = pipewire.ffi.new("struct spa_video_info *")

    pipewire.lib.pw_init(pipewire.ffi.NULL, pipewire.ffi.NULL)

    loop = pipewire.lib.pw_main_loop_new(pipewire.ffi.NULL)

    cb_data = {"loop": loop, "format": fmt}
    cb_handle = make_stream_handle(cb_data)

    stream = pipewire.lib.pw_stream_new_simple(
        pipewire.lib.pw_main_loop_get_loop(loop),
        b"video-capture",
        pipewire.lib.pw_properties_new(
            pipewire.lib.PW_KEY_MEDIA_TYPE, pipewire.ffi.from_buffer(b"Video"),
            pipewire.lib.PW_KEY_MEDIA_CATEGORY, pipewire.ffi.from_buffer(b"Capture"),
            pipewire.lib.PW_KEY_MEDIA_ROLE, pipewire.ffi.from_buffer(b"Camera"),
            pipewire.ffi.NULL,
        ),
        stream_events,
        cb_handle,
    )
    cb_data["stream"] = stream

    # XXX: spa_pod_builder_add_object not available.
    # XXX: SPA_POD_Id, SPA_POD_CHOICE_ENUM_Id, SPA_POD_CHOICE_RANGE_Rectangle, SPA_POD_CHOICE_RANGE_Fraction not available.
    # XXX: SPA_RECTANGLE, SPA_FRACTION not available.
    pipewire.lib.spa_pod_builder_push_object(
        b,
        f,
        pipewire.lib.SPA_TYPE_OBJECT_Format,
        pipewire.lib.SPA_PARAM_EnumFormat,
    )
    pipewire.lib.spa_pod_builder_add(
        b,
        pipewire.ffi.cast("int", pipewire.lib.SPA_FORMAT_mediaType), pipewire.ffi.from_buffer(b"I"), pipewire.ffi.cast("int", pipewire.lib.SPA_MEDIA_TYPE_video),
        pipewire.ffi.cast("int", pipewire.lib.SPA_FORMAT_mediaSubtype), pipewire.ffi.from_buffer(b"I"), pipewire.ffi.cast("int", pipewire.lib.SPA_MEDIA_SUBTYPE_raw),
        pipewire.ffi.cast("int", pipewire.lib.SPA_FORMAT_VIDEO_format), pipewire.ffi.from_buffer(b"?eI"), pipewire.ffi.cast("int", 7),
        pipewire.ffi.cast("int", pipewire.lib.SPA_VIDEO_FORMAT_RGB),
        pipewire.ffi.cast("int", pipewire.lib.SPA_VIDEO_FORMAT_RGB),
        pipewire.ffi.cast("int", pipewire.lib.SPA_VIDEO_FORMAT_RGBA),
        pipewire.ffi.cast("int", pipewire.lib.SPA_VIDEO_FORMAT_RGBx),
        pipewire.ffi.cast("int", pipewire.lib.SPA_VIDEO_FORMAT_BGRx),
        pipewire.ffi.cast("int", pipewire.lib.SPA_VIDEO_FORMAT_YUY2),
        pipewire.ffi.cast("int", pipewire.lib.SPA_VIDEO_FORMAT_I420),
        pipewire.ffi.cast("int", pipewire.lib.SPA_FORMAT_VIDEO_size), pipewire.ffi.from_buffer(b"?rR"), pipewire.ffi.cast("int", 3),
        r_def, r_min, r_max,
        pipewire.ffi.cast("int", pipewire.lib.SPA_FORMAT_VIDEO_framerate), pipewire.ffi.from_buffer(b"?rF"), pipewire.ffi.cast("int", 3),
        f_def, f_min, f_max,
        pipewire.ffi.NULL,
    )
    params[0] = pipewire.lib.spa_pod_builder_pop(b, f)

    pipewire.lib.pw_stream_connect(
        stream,
        pipewire.lib.PW_DIRECTION_INPUT,
        pipewire.lib.PW_ID_ANY,
        pipewire.lib.PW_STREAM_FLAG_AUTOCONNECT | pipewire.lib.PW_STREAM_FLAG_MAP_BUFFERS,
        params,
        1,
    )

    pipewire.lib.pw_main_loop_run(loop)

    pipewire.lib.pw_stream_destroy(stream)
    pipewire.lib.pw_main_loop_destroy(loop)


if __name__ == "__main__":
    main()
