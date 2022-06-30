A demo of basic Linux device driver

Pre-requisite: kernel-devel

The driver will be added to /proc/modules and /proc/devices.

To test this driver:
   1) Get the major device number from /proc/devices or dmesg
   2) mknod /dev/demo0 c <major device number> 0
   3) cat /dev/demo0
