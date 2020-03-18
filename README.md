# BR_Internet_Radio
This is a simple Internet radio built using mpd/mpc and Flask with Buildroot.
It has been developed for Orange Pi Zero board, but testing was also performed in
virtual machines (Virt 64 and Vexpress-A9) emulated in QEMU.

## Building
To build the Linux image, enter the appropriate directory and run the "build.sh" script.
It should automatically download the buildroot, unpack it, configure and build the image.

## Running
In case of the real hardware (currently only Orange Pi Zero), you should transfer
the compiled files to the SD card. You may simply write the generated sdcard.img
to the card using `dd` tool.
### Simplified update for Orange Pi Zero
When updating the image, I usually simply copy the "zImage", "sun8i-h2-plus-orangepi-zero.dtb", and "boot.scr"
files from output/images directory to the first partition of the SD card, and unpack the output/images/rootfs.ext4 
file to the second partition (after erasing it first). That procedure leaves the "u-boot-sunxi-with-spl.bin"
loader not updated, but that's usually not a problem.
Of course you may update it using the `dd` tool (replace /dev/sdX with the name of the device corresponding to your SD card):

```
dd if=u-boot-sunxi-with-spl.bin of=/dev/sdX bs=1024 seek=8
```



### Running in virtual machine
To test your radio in a virtual machine, run the "runme" file in the appropriate directory.

## Using
After the machine starts, the radio should start playing the first station.
You may control the radio via simplistic web interface available on the 8810 TCP port.
In case of the virtual machines it is forwarded to the 8888 port on the host machine.
