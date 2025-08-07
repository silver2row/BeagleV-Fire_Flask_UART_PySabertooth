# BeagleV-Fire_Flask_UART_PySabertooth
This is a small set of scripts to build around the BeagleV-Fire (Linux) and UART

- install the `bb-imager-rs` technology from beagleboard.org
- install the Trixie image from their image writer for the BeagleV-Fire
- use a USB debug adapter to watch for specifics: https://docs.beagleboard.org/boards/beaglev/fire/02-quick-start.html#beaglev-fire-quick-start
- follow the instructions and use the correct adapter(s). Find your device under /dev/
- so, if it is `/dev/ttyUSB0`, install `tio` and `tio /dev/ttyUSB0`

- there are some specifics on building the image and booting into the image on beagleboard.org
- once we have a built and bootable image, let us sign in via `tio` and then enable ssh by changing the password
- then on the Trixie image, it should be as easy as ssh debian@192.168.7.2
- if you board, the BeagleV-Fire, does not respond to the IP Address, look up your IP Address and use that instead

- now, we have our bootable image and board ready
* `sudo apt update && sudo apt upgrade`
* `sudo apt install git python3 python3-venv python3-flask python3-serial`
* the last `apt` install is for serial, i.e. so we can alter UART commands

```
# After the build from apt is done...
1. use the src file in this repo to handle utilizing /dev/bone/uart/4
2. now, once we have configured the correct data in the file, we also need to write up some /templates/MY_FILE.html file
3. the .html file should read our flask application so when the flask application calls an IP Address and Port, our html file is listed
```

Please use a `venv` from python3 via `python3 -m venv .` in the src file and then `source bin/activate`

### Update
This should get you far, i.e. as this is Linux and not the baremetal applications that can be used on the BeagleV-Fire
