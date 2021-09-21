import math

import pipewire



PI_TWICE = 2.0*math.pi
DEFAULT_RATE = 44100
DEFAULT_CHANNELS = 2
DEFAULT_VOLUME = 0.7


def make_stream_handle(fct_name, extra_data):
    def cb():
        try:
            b = pipewire.lib.pw_stream_dequeue_buffer(extra_data["stream"])
            if b == pipewire.ffi.NULL:
                print("out of buffers")
                return

            buf = b.buffer
            dst = buf.datas[0].data
            if dst == pipewire.ffi.NULL:
                return
            dst = pipewire.ffi.cast("int16_t *", dst)

            stride = pipewire.ffi.sizeof("int16_t")*DEFAULT_CHANNELS
            n_frames = buf.datas[0].maxsize//stride

            for i in range(n_frames):
                extra_data["accumulator"] += PI_TWICE*440/DEFAULT_RATE
                extra_data["accumulator"] %= PI_TWICE

                val = int(math.sin(extra_data["accumulator"])*DEFAULT_VOLUME*16767.0)
                for c in range(DEFAULT_CHANNELS):
                    dst[i*DEFAULT_CHANNELS + c] = val

            buf.datas[0].chunk.offset = 0
            buf.datas[0].chunk.stride = stride
            buf.datas[0].chunk.size = n_frames*stride

            pipewire.lib.pw_stream_queue_buffer(extra_data["stream"], b)
        except KeyboardInterrupt:
            pipewire.lib.pw_main_loop_quit(extra_data["loop"])

    return pipewire.ffi.new_handle({fct_name: cb})


def main():
    stream_events = pipewire.ffi.new("struct pw_stream_events *")
    stream_events.version = pipewire.lib.PW_VERSION_STREAM_EVENTS
    stream_events.process = pipewire.lib.py_cb_pw_stream_event_process

    params = pipewire.ffi.new("struct spa_pod *[1]")

    buffer = pipewire.ffi.new("uint8_t[1024]")
    b = pipewire.ffi.new("struct spa_pod_builder *")
    b.data = buffer
    b.size = pipewire.ffi.sizeof(buffer)

    i = pipewire.ffi.new("struct spa_audio_info_raw *")
    i.format = pipewire.lib.SPA_AUDIO_FORMAT_S16
    i.channels = DEFAULT_CHANNELS
    i.rate = DEFAULT_RATE

    pipewire.lib.pw_init(pipewire.ffi.NULL, pipewire.ffi.NULL)

    loop = pipewire.lib.pw_main_loop_new(pipewire.ffi.NULL)

    cb_data = {"loop": loop, "accumulator": 0.0}
    cb_handle = make_stream_handle("process", cb_data)

    stream = pipewire.lib.pw_stream_new_simple(
        pipewire.lib.pw_main_loop_get_loop(loop),
        b"audio-src",
        pipewire.lib.pw_properties_new(
            pipewire.lib.PW_KEY_MEDIA_TYPE, pipewire.ffi.from_buffer(b"Audio"),
            pipewire.lib.PW_KEY_MEDIA_CATEGORY, pipewire.ffi.from_buffer(b"Playback"),
            pipewire.lib.PW_KEY_MEDIA_ROLE, pipewire.ffi.from_buffer(b"Music"),
            pipewire.ffi.NULL,
        ),
        stream_events,
        cb_handle,
    )
    cb_data["stream"] = stream

    params[0] = pipewire.lib.spa_format_audio_raw_build(
        b,
        pipewire.lib.SPA_PARAM_EnumFormat,
        i,
    )

    pipewire.lib.pw_stream_connect(
        stream,
        pipewire.lib.PW_DIRECTION_OUTPUT,
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
