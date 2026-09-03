# Programs

## OV9282

For testing the OV9282 camera, the `mjpeg_server_ov9282-mpp.py` script configures the 
sensor for the specified frame rate and uses the Rockchip hardware JPEG 
encoder `NV12 → mppjpegenc → JPEG` to stream at up to 120 FPS.