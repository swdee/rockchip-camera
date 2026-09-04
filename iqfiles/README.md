# IQ Tuning Files

Work in progress.

The current tuning files here are for bootstrapping the rkaiq_3A server and production tuning has not been done yet.


## OV9282

The following overlay fields define the naming scheme of the IQ file in `/etc/iqfiles`:
```
rockchip,camera-module-name = "ov9282";
rockchip,camera-module-lens-name = "default";
```
This maps to the file `/etc/iqfiles/ov9282_ov9282_default.json`.
