# ELYSIUM-XR LeoRover Dockers

## Description
This repository contains the docker containers to launch the Leo Rover with the ELYSIUM-XR project configuration. The docker containers are based on ROS 2 Jazzy and use the `rmw_zenoh_cpp` ROS 2 middleware to communicate with each other. 

Inside this repo you will find the following docker containers:

- `livox_docker_zenoh`: contains the Livox MID 360 3D LiDAR docker to launch the sensor
- `zenoh_docker`: contains the Zenoh router configuration and launches a Zenoh router 
- `leorover_description_zenoh_docker`: contains the Leo Rover URDF description with the inverted mount for the Livox LiDAR (ELYSIUM-XR project configuration) 
- `realsense_docker_zenoh`: contains the RGB-D Realsense D455 launch and config files to run the camera with ROS 2
- `zenoh_to_fastrtps_docker`: contains Python relay scripts that publish `cmd_vel` data from Zenoh to Fast DDS over Jazzy in ROS 2 
- `rtabmap_livox_docker_zenoh`: contains the installation of `rtabmap_ros` with a custom ROS2 workspace that launches RTAB-Map for the Livox MID 360 LiDAR. 

## Pre-requisites

This repo assumes the following:

1. The Leo rover has been mounted with the appropriate hardware configuration (ELYSIUM-XR project configuration)
2. A static IP has been assigned to the on-board Nvidia Jetson and Rasberry Pi for the LunaLab network
3. The ROS 2 environment variables have been properly configured

For more questions regarding the ELYSIUM-XR project configuration for the Leo rover and the above listed pre-requisites, please contact: 

```
Alexandre Frantz 
alexandre.frantz@uni.lu
```

## Part1 : First setup for Leo rover Docker containers

To launch all the docker containers and essentially initialize your ROS 2 nodes to work with the Leo you must first setup and configure the Docker containers on the Leo rover

1. Remotely connect to the rover via `ssh`

```bash
ssh <username>@<robot_ip>
```

2. Create a folder in side the `home/user` directory and clone the repo (`user` might be different depending on your Jetson config)

```bash 
mkdir LeoRover-Dockers && cd LeoRover-Dockers 
git clone https://github.com/snt-spacer/ELYSIUM-XR-LeoRover-Dockers.git
```

3. Setup environment variables for the Jetson in the `.bashrc`

Add the two lines at the end: 

```bash
export ROS_DOMAIN_ID=X
export ROS_NAMESPACE=""
```
Where `X` is the Leo Rover number and the namespace is `leo0X` (same choice as the domain id for `X`). For example, if you Leo rover is labeled as `Leo-06`, then `ROS_DOMAIN_ID=6` and `ROS_NAMESPACE="leo06"`.

4. Navigate to each docker container and build them (see README.md for each docker container)

Example (for each docker container): 

```bash
cd LeoRover-Dockers/ELYSIUM-XR-LeoRover-Dockers/leorover_description_zenoh_docker/docker
bash ./docker_build.sh
```
> Hint: Make sure you are connected to internet when building the docker containers, as you are pulling the `ros-jazzy` image and related ROS 2 packages.

### (Optional) If building on Nvidia Jetson Xavier NGX Tips 


### FIX: Default power mode throttling performance

When building the `livox_docker_zenoh` docker container, it is recommended to check your board's power mode. 

```bash
sudo nvpmodel -q 
```

If this output is anything else but this: 

```
MODE_20W_6CORE
8
```

Then make sure you switch your power mode to 20W with all 6 cores enabled by running this command: 

```bash
sudo nvpmodel -m 8
```

## Part 2: Configuring the Dockers for your Leo Rover

Once you have built all the Docker containers, we now need to configure certain files to make the containers run for the specific Leo rover you are using. Since each Leo rover is identified with `Leo-0X`, where `X` is the ID of the rover, we need to proceed as follows.

### Update Robot Description with your Leo Rover namespace

1. Navigate to:

```bash
cd ELYSIUM-XR-LeoRover-Dockers/leorover_description_zenoh_docker/ros2_ws/src/leo_description/urdf
vim leo.urdf.xacro
```

And

```bash
cd ELYSIUM-XR-LeoRover-Dockers/leorover_description_zenoh_docker/ros2_ws/src/leo_description/launch
vim state_publisher.launch.xml 
```

2. Edit these two files by changing `leo04` to `leoX`, where `X` is your Leo Rover number

### Change Livox Configuration to match the LiDAR and Jetson used
 
1. Change Livox MID 360 configuration (see `livox_docker_zenoh` README for more details).

```bash
cd /home/spacer/LeoRover-Docker-Containers/ELYSIUM-XR-LeoRover-Dockers/livox_docker_zenoh/ros2_ws/src/livox_ros_driver2/
vim MID360_config.json
```

Change `MID360_config.json` to point to the LiDAR IP address on `192.168.1.XXX`, where `XXX` is the LiDAR IP. You also need to change the `HOST_IP` to point to the IP-address of the Jetson on the same subnet (Usually it will be `192.168.1.X`, where `X` is the Leo rover ID).


2. Change launch file for MID360

```bash
cd /home/spacer/LeoRover-Docker-Containers/ELYSIUM-XR-LeoRover-Dockers/livox_docker_zenoh/ros2_ws/src/livox_ros_driver2/launchROS2/
vim MID360_launch.py
```

Change `frame_id` to the one for your Leo Rover (for example if using `Leo08` -> `leo08/livox_frame`)


### Change Zenoh to Fast DDS cmd_vel topic

1. Go to `ELYSIUM-XR-LeoRover-Dockers/zenoh_to_fastrtps_docker/docker` 

```bash
cd ELYSIUM-XR-LeoRover-Dockers/zenoh_to_fastrtps_docker/docker
```

2. Open the `entrypoint.sh` file and change the parameter `--topic` to the `cmd_vel` topic corresponding to you robot

```bash
vim entrypoint.sh
```

## Part 3: Working with the Leo rover

Once the docker containers are running on the rover, go ahead and start your Zenoh router on the remote PC. This Zenoh router connects to the one on the Leo rover, allowing you to visualize the ROS 2 topics from the rover.

In a new terminal execute:

```bash

export RMW_IMPLEMENTATION=rmw_zenoh_cpp

export ZENOH_CONFIG_OVERRIDE='connect/endpoints=["tcp/192.168.88.XXX:7447"]'

export ROS_DOMAIN_ID=X

ros2 run rmw_zenoh_cpp rmw_zenohd
```

> Hint 1: if you haven't downloaded Zenoh for ROS 2 yet, go to this link:https://docs.ros.org/en/jazzy/Installation/RMW-Implementations/Non-DDS-Implementations/Working-with-Zenoh.html

> Hint 2: The IP-address for the `ZENOH_CONFIG_OVERRIDE` should be the correct IP address of your Leo Rover. The format is usually `192.168.88.1X3`, where `X` is the number ID of the Leo Rover (sticker on the back).

Once you have the Zenoh router running, go ahead and check if the topics are visible:

```bash
ros2 topic list 
```

You should see something along the lines of: 

```
/leo0X/cmd_vel
/leo0X/livox/lidar
/leo0X/cloud_map
....
```

> CAUTION: The LiDAR topic can take some time to appear and populate with data, therefore you can wait a couple of minutes. 
