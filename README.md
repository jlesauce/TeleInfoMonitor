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
cat /proc/device-tree/model
Raspberry Pi Zero W Rev 1.1
```

OS version:

```shell
cat /etc/os-release
PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
```

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
stty -F /dev/ttyAMA0 1200 sane evenp parenb cs7 -crtscts
cat /dev/ttyAMA0
```

This should output the data collected from Linky. If nothing returned, then serial link is probably
not well configured.
