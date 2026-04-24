# Zenoh to Fast RTPS Docker

## Description
This repostory contains the files to build a Docker image that contains two scripts for driving the Leo Rover through the ROS2 Zenoh middleware `rmw_zenoh_cpp`. Since the Leo Rover is build on the Micro XRCE Controller (based on  Fast DDS), we need to send velocity commands from zenoh to fast. This docker is based on ROS2 Jazzy.

## Getting started
Simply clone the parent git repository:

```bash
git clone clone https://github.com/snt-spacer/ELYSIUM-XR-LeoRover-Dockers.git
```

Then, enter the `docker` directory:

```bash
cd zenoh_to_fastrtps_docker/docker/
```

Now, build the Docker image:

```
bash ./docker_build.sh
```

And run the container from within the `docker` directory:

```bash
bash ./docker_run.sh
```


## Usage
- Inside the repository, there is a file called `docker_build.sh`. When running this script, it will create a Docker image. 
- There is another script called `docker_run.sh`. When running this script, a Docker container will be started that starts the Realsense Camera.
- This container will persist reboots and restarts automatically. To stop the container, use The script called `docker_stop.sh`.


## Project structure
This repository contains a `relays` folder inside the docker container. The folowing two scripts are executed when the container is started:

1. `cmdvel_fastrx.py`: a Python script that reads a UDP socket on the host machine and send data to the appropriate ROS2 topic using FastDDS. in this case, it is velocity commands from `/leo0X/cmd_vel` from Zenoh and retransmitted to the same topic via FastDDS
2. `cmdvel_zenohtx.py` A python scripts that publishes into a UDP socket on the host machine and sends velocity data from the `/leo0X/cmd_vel` from Zenoh. The listener in the receiving side republishes into the same topic using FastDDS.

To allow the Docker container to communicate with the host machine and with remote devices, the file `docker/config/fastrtps-profile.xml` changes the DDS settings accordingly. Therefore, the system memory will be made accessible when running the container by usong the flags `--network host --ipc host --volume "/dev/shm:/dev/shm"`. They allow for the Docker container to communicate with other ROS 2 nodes as if it was running directly on the host.

**Note:** For changes in the file `entrypoint.sh`, the Docker image needs to be rebuilt as it is copied into the image and not mounted when running the container.


## Setting ROS environmental variables

The Docker container will take over the environmental variables of the host system for the `ROS_DOMAIN_ID`, the `ROS_NAMESPACE` and for the `ROS_LOCALHOST_ONLY` settings. This way, the `ROS_DOMAIN_ID` can easily be changed if needed for certain experiments and the `ROS_NAMESPACE` can be globally set for a robot and does not need to be adapted inside this repository, allowing for easily deploying the exact same repository on different robots with different namespaces and domain IDs without additional configuration by the user.