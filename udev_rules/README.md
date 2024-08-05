# UDEV Rules

## 1) Tools Used

* udevadm - udev management tool [(man page)](https://www.man7.org/linux/man-pages/man8/udevadm.8.html)

## 2) Usage

### i) Getting info
```
udevadm info /dev/ttyUSBX
```

### ii) Writing Udev Rules

1) Adding subsystem
```
SUBSYSTEM="tty"
```

2) Adding matching

- using regex to make matching more flexible (e.g. [0-9] to match any number, * to match anything at all).

```
KERNEL=="ttyUSB[0-9]*"
```

3) Adding vendor id

- in udevadm info output as `ID_VENDOR_ID`

```
ATTRS{idVendor}=="0403"
```

4) Adding product id

- in udevadm info output as `ID_MODEL_ID`

```
ATTRS{idProduct}=="6001"
```

5) Adding serial id

- in udevadm info output as `ID_SERIAL` or `ID_SERIAL_SHORT`

```
ATTRS{serial}=="B002GH62"
(or)
ATTRS{serial}=="FTDI_FT232R_USB_UART_B002GH62"
```

6) Adding mode

- Set permissions to allow any user read/write access to the device.

```
MODE="0666"
```

7) Adding symlink name

- It create a symlink in /dev/ for this device.
```
SYMLINK+="tty_battery_plug"
```

### iii) Running the new udev rule

```
sudo udevadm control --reload-rules && sudo service udev restart && sudo udevadm trigger
```

## 3) Issues

### Action as add prevents multi devices
- Cause
    - Unknown
- Solution 
    - Not using `ACTION` at all.

```
ACTION=="add"
```

## 4) Resources

1) https://www.clearpathrobotics.com/assets/guides/kinetic/ros/Udev%20Rules.html
2) https://opensource.com/article/18/11/udev
3) https://www.man7.org/linux/man-pages/man8/udevadm.8.html