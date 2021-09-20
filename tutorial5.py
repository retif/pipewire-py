import pipewire



def make_stream_handle(extra_data):
    def cb_process():
        try:
            b = pipewire.libp.pw_stream_dequeue_buffer(extra_data["stream"])
            if b == pipewire.ffip.NULL:
                print("out of buffers")
                return

            buf = b.buffer
            if buf.datas[0].data == pipewire.ffip.NULL:
                return

            print(f"got a frame of size {buf.datas[0].chunk.size}")

            pipewire.libp.pw_stream_queue_buffer(extra_data["stream"], b)
        except KeyboardInterrupt:
            pipewire.libp.pw_main_loop_quit(extra_data["loop"])

    def cb_param_changed(id, param):
        try:
            if param == pipewire.ffis.NULL or id != pipewire.libs.SPA_PARAM_Format:
                return

            if pipewire.libs.spa_format_parse(param, pipewire.ffis.addressof(extra_data["format"], "media_type"), pipewire.ffis.addressof(extra_data["format"], "media_subtype")) < 0:
                return

            if extra_data["format"].media_type != pipewire.libs.SPA_MEDIA_TYPE_video or extra_data["format"].media_subtype != pipewire.libs.SPA_MEDIA_SUBTYPE_raw:
                return

            if pipewire.libs.spa_format_video_raw_parse(param, pipewire.ffis.addressof(extra_data["format"].info, "raw")) < 0:
                return

            print("got video format:");
            print(f"  format: {extra_data['format'].info.raw.format} ({pipewire.ffis.string(pipewire.libs.spa_debug_type_find_name(pipewire.libs.spa_type_video_format, extra_data['format'].info.raw.format)).decode()})")
            print(f"  size: {extra_data['format'].info.raw.size.width}x{extra_data['format'].info.raw.size.height}")
            print(f"  framerate: {extra_data['format'].info.raw.framerate.num}/{extra_data['format'].info.raw.framerate.denom}")
        except KeyboardInterrupt:
            pipewire.libp.pw_main_loop_quit(extra_data["loop"])

    return pipewire.ffip.new_handle({"process": cb_process, "param_changed": cb_param_changed})


def main():
    stream_events = pipewire.ffip.new("struct pw_stream_events *")
    stream_events.version = pipewire.libp.PW_VERSION_STREAM_EVENTS
    stream_events.process = pipewire.libp.py_cb_pw_stream_event_process
    stream_events.param_changed = pipewire.libp.py_cb_pw_stream_event_param_changed

    params = pipewire.ffis.new("struct spa_pod *[1]")

    buffer = pipewire.ffis.new("uint8_t[1024]")
    b = pipewire.ffis.new("struct spa_pod_builder *")
    b.data = buffer
    b.size = pipewire.ffis.sizeof(buffer)

    f = pipewire.ffis.new("struct spa_pod_frame *")

    r_def = pipewire.ffis.new("struct spa_rectangle *")
    r_def.width = 320
    r_def.height = 240
    r_min = pipewire.ffis.new("struct spa_rectangle *")
    r_min.width = 1
    r_min.height = 1
    r_max = pipewire.ffis.new("struct spa_rectangle *")
    r_max.width = 4096
    r_max.height = 4096

    f_def = pipewire.ffis.new("struct spa_fraction *")
    f_def.num = 25
    f_def.denom = 1
    f_min = pipewire.ffis.new("struct spa_fraction *")
    f_min.num = 0
    f_min.denom = 1
    f_max = pipewire.ffis.new("struct spa_fraction *")
    f_max.num = 1000
    f_max.denom = 1

    fmt = pipewire.ffis.new("struct spa_video_info *")

    pipewire.libp.pw_init(pipewire.ffip.NULL, pipewire.ffip.NULL)

    loop = pipewire.libp.pw_main_loop_new(pipewire.ffip.NULL)

    cb_data = {"loop": loop, "format": fmt}
    cb_handle = make_stream_handle(cb_data)

    stream = pipewire.libp.pw_stream_new_simple(
        pipewire.libp.pw_main_loop_get_loop(loop),
        b"video-capture",
        pipewire.libp.pw_properties_new(
            pipewire.libp.PW_KEY_MEDIA_TYPE, pipewire.ffip.from_buffer(b"Video"),
            pipewire.libp.PW_KEY_MEDIA_CATEGORY, pipewire.ffip.from_buffer(b"Capture"),
            pipewire.libp.PW_KEY_MEDIA_ROLE, pipewire.ffip.from_buffer(b"Camera"),
            pipewire.ffip.NULL,
        ),
        stream_events,
        cb_handle,
    )
    cb_data["stream"] = stream

    # XXX: spa_pod_builder_add_object not available.
    # XXX: SPA_POD_Id, SPA_POD_CHOICE_ENUM_Id, SPA_POD_CHOICE_RANGE_Rectangle, SPA_POD_CHOICE_RANGE_Fraction not available.
    # XXX: SPA_RECTANGLE, SPA_FRACTION not available.
    pipewire.libs.spa_pod_builder_push_object(
        b,
        f,
        pipewire.libs.SPA_TYPE_OBJECT_Format,
        pipewire.libs.SPA_PARAM_EnumFormat,
    )
    pipewire.libs.spa_pod_builder_add(
        b,
        pipewire.ffip.cast("int", pipewire.libp.SPA_FORMAT_mediaType), pipewire.ffip.from_buffer(b"I"), pipewire.ffip.cast("int", pipewire.libp.SPA_MEDIA_TYPE_video),
        pipewire.ffip.cast("int", pipewire.libp.SPA_FORMAT_mediaSubtype), pipewire.ffip.from_buffer(b"I"), pipewire.ffip.cast("int", pipewire.libp.SPA_MEDIA_SUBTYPE_raw),
        pipewire.ffip.cast("int", pipewire.libp.SPA_FORMAT_VIDEO_format), pipewire.ffip.from_buffer(b"?eI"), pipewire.ffip.cast("int", 7),
        pipewire.ffip.cast("int", pipewire.libp.SPA_VIDEO_FORMAT_RGB),
        pipewire.ffip.cast("int", pipewire.libp.SPA_VIDEO_FORMAT_RGB),
        pipewire.ffip.cast("int", pipewire.libp.SPA_VIDEO_FORMAT_RGBA),
        pipewire.ffip.cast("int", pipewire.libp.SPA_VIDEO_FORMAT_RGBx),
        pipewire.ffip.cast("int", pipewire.libp.SPA_VIDEO_FORMAT_BGRx),
        pipewire.ffip.cast("int", pipewire.libp.SPA_VIDEO_FORMAT_YUY2),
        pipewire.ffip.cast("int", pipewire.libp.SPA_VIDEO_FORMAT_I420),
        pipewire.ffip.cast("int", pipewire.libp.SPA_FORMAT_VIDEO_size), pipewire.ffip.from_buffer(b"?rR"), pipewire.ffip.cast("int", 3),
        r_def, r_min, r_max,
        pipewire.ffip.cast("int", pipewire.libp.SPA_FORMAT_VIDEO_framerate), pipewire.ffip.from_buffer(b"?rF"), pipewire.ffip.cast("int", 3),
        f_def, f_min, f_max,
        pipewire.ffip.NULL,
    )
    params[0] = pipewire.libs.spa_pod_builder_pop(b, f)

    pipewire.libp.pw_stream_connect(
        stream,
        pipewire.libp.PW_DIRECTION_INPUT,
        pipewire.libp.PW_ID_ANY,
        pipewire.libp.PW_STREAM_FLAG_AUTOCONNECT | pipewire.libp.PW_STREAM_FLAG_MAP_BUFFERS,
        params,
        1,
    )

    pipewire.libp.pw_main_loop_run(loop)

    pipewire.libp.pw_stream_destroy(stream)
    pipewire.libp.pw_main_loop_destroy(loop)


if __name__ == "__main__":
    main()
