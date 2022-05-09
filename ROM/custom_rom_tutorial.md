# Tutorial
### Requirements
- a (virtual) linux device that runs armel code (f.e. a Raspberry Pi)
- docker engine -> https://docs.docker.com/engine/install/
- root access
- brickstrap -> https://github.com/ev3dev/brickstrap

### Steps
Get an official image

    sudo docker pull ev3dev/ev3dev-bullseye-ev3-generic

Start a shell as the `robot` user

    sudo docker run -it ev3dev/ev3dev-bullseye-ev3-generic su -l robot

Edit the `/etc/apt/sources.list` file

    sudo nano /etc/apt/sources.list

The default password is `maker`

Add these lines:

    deb http://ftp.debian.org/debian stretch main contrib non-free
    deb http://security.debian.org/ bullseye-security/updates main contrib non-free

Update and upgrade the system (this might take some time)

    sudo apt update
    sudo apt full-upgrade -y

Install `pybricks-micropython` and `pip` (required for controlling the robot with python)

    sudo apt install pybricks-micropython pip -y

Install the python library pybricks

    pip install pybricks

The brickstrap tool will overwrite `/etc/apt/sources.list`. If you want to keep the current configuration (I recommend this) execute the following command:

    sudo cp /etc/apt/sources.list /brickstrap/_tar-only/etc/apt/sources.list

Now you can customize the rom  

After that exit the docker container

    exit

Find the container you just created. You need the container id or name

    sudo docker container ls -a

Example output:

    CONTAINER ID   IMAGE                                COMMAND         CREATED             STATUS                      PORTS     NAMES
    c06d57b783bf   ev3dev/ev3dev-bullseye-ev3-generic   "su -l robot"   About an hour ago   Exited (0) 17 seconds ago             optimistic_curran

Create a new image of the container. Replace `CONTAINER` with the container id or name

    sudo docker container commit CONTAINER custom_ev3_rom

Create the image

    sudo brickstrap create-tar custom_ev3_rom custom_ev3_rom.tar
    sudo brickstrap create-image custom_ev3_rom.tar custom_ev3_rom.img

Now you have a customized bootable image