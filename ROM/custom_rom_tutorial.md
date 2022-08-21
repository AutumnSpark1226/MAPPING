# Tutorial
### Requirements
- a (virtual) linux device that runs armel code (e.g. a Raspberry Pi)
- docker engine -> https://docs.docker.com/engine/install/
- brickstrap -> https://github.com/ev3dev/brickstrap

### Steps
Get an official image

    sudo docker pull ev3dev/ev3dev-stretch-ev3-generic

Start a shell as the `robot` user

    sudo docker run -it ev3dev/ev3dev-stretch-ev3-generic su -l robot

Update and upgrade the system (this might take some time)

The default password is `maker`

    sudo apt update
    sudo apt full-upgrade -y

Install `pip`

    sudo apt install python3-pip -y

Test it (did not work for me) and install `pybricks`

    pip install pybricks

If it installed pybricks, skip this step

    curl https://bootstrap.pypa.io/pip/3.5/get-pip.py > get-pip.py
    python3 get-pip.py
    python3 -m pip install pybricks

Now you can customize the rom  

After that exit the docker container

    exit

Find the container you just created. You need the container id or name

    sudo docker container ls -a

Example output:

    CONTAINER ID   IMAGE                                COMMAND         CREATED             STATUS                      PORTS     NAMES
    c06d57b783bf   ev3dev/ev3dev-stretch-ev3-generic   "su -l robot"   About an hour ago   Exited (0) 17 seconds ago             optimistic_curran

Create a new image of the container. Replace `CONTAINER` with the container id or name

    sudo docker container commit CONTAINER custom_ev3_rom

Create the image

    sudo brickstrap create-tar custom_ev3_rom custom_ev3_rom.tar
    sudo brickstrap create-image custom_ev3_rom.tar custom_ev3_rom.img

Now you have a customized bootable image