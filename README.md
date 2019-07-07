# OctoPrint-Enclosure

- Use this plugin to automatically turn on and off leds. (At the start of a timelapse for example)
- Read the temperature of the enclosure.
- Turn on and off leds by using a button.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/wouterbruggeman/EnclosurePlugin/archive/master.zip

After downloading the plugin, execute the following steps:
1. Login to your Raspberry pi using ssh.
2. Enter ``sudo raspi-config`` and go to Advanced Options -> 1-Wire -> Yes. To enable 1-Wire.
3. Reboot the device and check if the module is started with ``lsmod | grep w1``. If the module is 
started, skip to 5.
4. Mount the device with ``sudo modprobe w1_gpio && sudo modprobe w1_therm``
5.  Configure the device name in the plugin settings in Octoprint. The name of the device can 
be found with ``ls /sys/bus/w1/devices/`` and should be starting with '28'.
6. Restart the Octoprint server and everything should be working at this point.

The following circuit has to be build:
![circuit][https://github.com/wouterbruggeman/EnclosurePlugin/schemes/circuit.png]

## Warning
This program may contain bugs. I (Wouter Bruggeman) am not responsible for anything that happens
to you, your printer or anything else. Use this program at your own risk!

## Known bugs:
- After starting octoprint with ``octoprint serve`` the user is unable to exit the program by 
using CTRL+C
