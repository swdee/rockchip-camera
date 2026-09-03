#!/usr/bin/env python3

import subprocess
import time

from flask import Flask, Response
import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst


DEVICE = "/dev/video11"
SENSOR = "/dev/v4l-subdev2"

WIDTH = 1280
HEIGHT = 800
FPS = 120

app = Flask(__name__)

Gst.init(None)


def set_sensor_fps(fps):
    # OV9282 1280x800:
    # 120 fps corresponds to VTS = 910
    vts = round(910 * 120 / fps)
    vblank = vts - HEIGHT

    if vblank < 110:
        vblank = 110

    print(
        f"Setting sensor to approximately {fps} FPS: "
        f"VTS={vts}, VBLANK={vblank}"
    )

    subprocess.run(
        [
            "v4l2-ctl",
            "-d", SENSOR,
            f"--set-ctrl=vertical_blanking={vblank}",
        ],
        check=True,
    )


set_sensor_fps(FPS)

PIPELINE = (
    f"v4l2src device={DEVICE} io-mode=2 ! "
    f"video/x-raw,format=NV12,width={WIDTH},height={HEIGHT} ! "
    "mppjpegenc ! "
    "appsink name=sink "
    "drop=true "
    "max-buffers=2 "
    "sync=false"
)

print("Opening pipeline:")
print(PIPELINE)

pipeline = Gst.parse_launch(PIPELINE)
sink = pipeline.get_by_name("sink")

pipeline.set_state(Gst.State.PLAYING)


def frames():
    frame_number = 0
    fps_frames = 0
    fps_start = time.monotonic()

    while True:
        sample = sink.emit("pull-sample")

        if sample is None:
            print("Failed to get GStreamer sample")
            time.sleep(0.01)
            continue

        buffer = sample.get_buffer()

        success, map_info = buffer.map(Gst.MapFlags.READ)

        if not success:
            continue

        try:
            jpg = bytes(map_info.data)
        finally:
            buffer.unmap(map_info)

        frame_number += 1
        fps_frames += 1

        now = time.monotonic()
        elapsed = now - fps_start

        if elapsed >= 1.0:
            print(
                f"JPEG FPS: {fps_frames / elapsed:.2f} "
                f"(total frames: {frame_number}, "
                f"JPEG size: {len(jpg)} bytes)"
            )

            fps_frames = 0
            fps_start = now

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n"
            b"Cache-Control: no-cache\r\n\r\n"
            + jpg
            + b"\r\n"
        )


@app.route("/")
def index():
    return """
    <html>
      <body style="margin:0;background:#000">
        <img src="/stream.mjpg"
             style="width:100%;height:auto">
      </body>
    </html>
    """


@app.route("/stream.mjpg")
def stream():
    return Response(
        frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    try:
        app.run(
            host="0.0.0.0",
            port=8080,
            threaded=True,
            debug=False,
        )
    finally:
        pipeline.set_state(Gst.State.NULL)
