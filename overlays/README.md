# Camera Overlays


## RK3576 - Radxa Rock 4D

* OV9281 - For [Waveshare OV9281-160 Camera](https://www.waveshare.com/product/raspberry-pi/cameras/global-shutter-cameras/ov9281-160-camera.htm)
  It would also work for the other FOV variations at 110 and 120 degrees.
* IMX290 - For [Waveshare IMX290 2MP Camera \(A\)](https://www.waveshare.com/product/raspberry-pi/cameras/2m-pixels/imx290-2mp-camera-a.htm)

## RK3576 - Radxa CM4

* OV9282 - For [Arducam B0329](https://www.arducam.com/arducam-1mp-ov9282-fisheye-mono-global-shutter-drop-in-replacement-for-depthai-oak-dnoir.html)  
  Note that the OV9282's default I2C address is 0x60 however Arducam wired the SID input pin high so it identifies itself at address 0x10.