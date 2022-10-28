# TeleInfo Monitor

Application used to monitor the user data transmitted by Linky meter system used by French national energy
provider.

# Hardware Configuration

## Material

* Raspberry Pi Zero
  W ([Buy one](https://www.kubii.fr/les-cartes-raspberry-pi/1851-raspberry-pi-zero-w-kubii-3272496006997.html))
* PiTInfo shield for Linky user
  interface ([Buy one](https://www.tindie.com/products/Hallard/pitinfo/))

## Raspberry Pi Zero

### Version

Board version:

```shell
$ cat /proc/device-tree/model
Raspberry Pi Zero W Rev 1.1
```

OS version:

```shell
$ cat /etc/os-release
PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
```

### How to plug the PiTInfo module

The PiTInfo module should be plugged on GPIO pins {1..10} like in below picture:

<img src="https://www.jonathandupre.fr/images/articles/2018/208/08.jpg" alt="image_pitinfo_plugged" style="width:400px;"/>

For information, the full mapping of GPIOs can be found here:
[model-zerow-rev1](https://pi4j.com/1.2/pins/model-zerow-rev1.html)

Pin 8 and 10, respectively GPIO 15 and 16 corresponds to the UART, which means where we get the serial data from Enedis
meter.

### Serial Link Configuration

* Disable serial console:
    - Edit /boot/cmdline.txt
    - Remove line: `console=serial0,(...)`
* Disable bluetooth module:
    - Edit /boot/config.txt
    - Add line: `dtoverlay=pi3-miniuart-bt`
* Reboot raspberry.

### How to test serial link

```shell
$ sudo stty -F /dev/ttyAMA0 1200 sane evenp parenb cs7 -crtscts
$ sudo chmod 666 /dev/ttyAMA0
$ sudo cat /dev/ttyAMA0
```

This should output the data collected from Linky. If nothing returned, then serial link is probably
not well configured.
