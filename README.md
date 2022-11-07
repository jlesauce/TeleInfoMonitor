# TeleInfo Monitor

Application used to monitor the user data transmitted by Linky meter system used by French national energy
provider.

## Hardware Description

### Material

* Raspberry Pi Zero
  W ([Buy one](https://www.kubii.fr/les-cartes-raspberry-pi/1851-raspberry-pi-zero-w-kubii-3272496006997.html))
* PiTInfo shield for Linky user
  interface ([Buy one](https://www.tindie.com/products/Hallard/pitinfo/))

### Raspberry Pi Zero

#### Version

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

## Serial Link Configuration

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

## How to create database on Raspberry

### Install MariaDB server locally

```shell
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install mariadb-server
$ sudo apt install libmariadbclient-dev # For python bindings
$ sudo apt install libmariadb3 libmariadb-dev # For python3 mariadb connectors
```

### Create and configure database

#### Creation

Secure and configure mysql:

```shell
$ sudo mysql_secure_installation # Say yes to all
$ sudo mysql -u root -p
```

Create database:

```mariadb
CREATE DATABASE teleinfodb;
CREATE USER 'jlesauce'@'<remote-ip-address>' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON teleinfodb.* TO 'jlesauce'@'<remote-ip-address>';
FLUSH PRIVILEGES;
```

#### Configuration

Enable remote access to database:

In file `/etc/mysql/mariadb.conf.d/50-server.cnf`, change line `bind-address = 127.0.0.1` to `bind-address = *`

```shell
$ sudo service mysql restart
```

To connect remotely:

```shell
$ mysql -u jlesauce -p -h <raspberry-ip-address>
```

#### Creating the DB schema and table

```mariadb
create schema teleinfodb;
use teleinfodb;
create table teleinfoframes
(
    timestamp                    TIMESTAMP not null comment 'Frame timestamp in format YYYY-MM-DD HH:mm:ss.zzzzzz',
    meter_identifier             CHAR(12)  not null comment 'Identifier of Enedis telemeter',
    subscription_type            CHAR(4)   not null comment 'Customer subscription mode',
    subscription_power_in_a      INT       not null comment 'Power in amperes',
    total_base_index_in_wh       INT       not null comment 'Total base index in W.h',
    current_pricing_period       CHAR(4)   not null comment 'Current period if using peak/off-peak pricing',
    instantaneous_intensity_in_a INT       not null comment 'Current intensity in amperes',
    intensity_max_in_a           INT       not null comment 'Maximum intensity in amperes',
    power_consumption_in_va      INT       not null comment 'Power consumption in V.A',
    peak_off_peak_schedule       CHAR      not null comment 'Peak/Off-peak time schedule',
    meter_state_code             CHAR(6)   null comment 'Error code returned by telemeter',
    constraint teleinfoframes_pk
        primary key (timestamp)
) comment 'Table containing the teleinfo frames'
```
