# Drivers

This driver source belongs in src/drivers/media/i2c/ when building kernel.

Currently tested on RK3576 (Radxa Rock 4D).


## Camera Support

IMX290 driver developed with [Waveshare IMX290 2MP Camera \(A\)](https://www.waveshare.com/product/raspberry-pi/cameras/2m-pixels/imx290-2mp-camera-a.htm)

OV9282 driver developer with [Arducam B0329](https://www.arducam.com/arducam-1mp-ov9282-fisheye-mono-global-shutter-drop-in-replacement-for-depthai-oak-dnoir.html) 
module and custom carrier board.



## OV9282 Driver

This driver has been patched to support the sensors 30/60/120 FPS rates at 1280x800.

Setting FPS is done by changing the VBLANK value with;
```
# 60 fps
v4l2-ctl -d /dev/v4l-subdev2 \
  --set-ctrl=vertical_blanking=1020

# 30 fps
v4l2-ctl -d /dev/v4l-subdev2 \
  --set-ctrl=vertical_blanking=2840

# 120 fps
v4l2-ctl -d /dev/v4l-subdev2 \
  --set-ctrl=vertical_blanking=110
```

Then verify using GStreamer the FPS rate;
```
gst-launch-1.0 -v \
    v4l2src device=/dev/video11 io-mode=2 ! \
    video/x-raw,format=NV12,width=1280,height=800 ! \
    fpsdisplaysink video-sink=fakesink text-overlay=false sync=false
```