# Custom ROM

### Status: `not tested`
### Version: `20221006`

## TODO
- install apt-utils dialog htop ufw zsh clang g++ python3-pip
- install pybricks (pip)
- set login shell
- configure zsh
- replace PATH in .zshrc
- password
- sshd configuration: port 22022; some security settings
- clone this repo
- set standard hostname (mappingX) in `/brickstrap/_tar-only/etc/hostname`
- rtl8188eu driver workaround: https://github.com/ev3dev/ev3dev/wiki/USB-Wi-Fi-Dongles


     /etc/udev/rules.d/99-edimax-n150-eu.rules


     ACTION=="add", ATTRS{idVendor}=="b811", ATTRS{idProduct}=="331b", RUN+="/sbin/modprobe 8188eu" RUN+="/bin/sh -c 'echo 7392 b811 > /sys/bus/usb/drivers/r8188eu/new_id'"


## TODO after flashing
- set hostnames (mapping0, mapping1)
- configure ufw
- pybricks-micropython pip/pycryptodomex????
