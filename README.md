# ELYSIUM-XR LeoRover Dockers

## Description
This repository contains the docker containers to launch the Leo Rover with the inverted LiDAR configuration. The docker containers are based on ROS 2 Jazzy and use the `rmw_zenoh_cpp` ROS 2 middleware to communicate with each other. 

Inside this repo you will find the following docker containers:

- `livox_docker_zenoh`: contains the Livox MID 360 3D LiDAR docker to launch the sensor
- `zenoh_docker`: contains the Zenoh router configuration and launches a Zenoh router 
- `leorover_description_zenoh_docker`: contains the Leo Rover URDF description with the inverted mount for the Livox LiDAR 
- `realsense_docker_zenoh`: contains the RGB-D Realsense D455 launch and config files to run the camera with ROS 2
- `zenoh_to_fastrtps_docker`: contains Python relay scripts that publish `cmd_vel` data from Zenoh to Fast DDS over Jazzy in ROS 2 
- `rtabmap_livox_docker_zenoh`: contains the installation of `rtabmap_ros` with a custom ROS2 workspace that launched RTAB-Map for the Livox MID 360 LiDAR. 

## Launching the docker containers

To launch all the docker containers and essentially initialize your ROS 2 nodes to work with the Leo you must first start the Zenoh router on the rover

1. Remotely connect to the rover via `ssh`

```bash
ssh <username>@<robot_ip>
```

2. Create a folder in side the `home` directory and clone the repo

```bash 
mkdir LeoRover-Dockers && cd LeoRover-Dockers 
git clone https://github.com/snt-spacer/ELYSIUM-XR-LeoRover-Dockers.git
```

3. Navigate to each docker container, build them, and launch them (see README.md for each docker container)

4. Once the docker containers are running on the rover, go ahead and start your Zenoh router on the remote PC. This Zenoh router connects to the one on the Leo rover, allowing you to visualize the ROS 2 topics from the rover.

In a new terminal execute:

```bash

export RMW_IMPLEMENTATION=rmw_zenoh_cpp

export ZENOH_CONFIG_OVERRIDE='connect/endpoints=["tcp/192.168.88.143:7447"]'

ros2 run rmw_zenoh_cpp rmw_zenohd
```

> Hint 1: if you haven't downloaded Zenoh for ROS 2 yet, go to this link:https://docs.ros.org/en/jazzy/Installation/RMW-Implementations/Non-DDS-Implementations/Working-with-Zenoh.html


> Hint 2: Don't forget to set your `ROS_DOMAIN_ID` environment variable as well, if applicable to your use case


## Nvidia Jetson Xavier NGX Tips 


### FIX: Default power mode throttling performance

When building the `livox_docker_zenoh` docker container, it is recommended to check your board's power mode. 

```bash
sudo nvpmodel -q 
```

If this output is anything else but this: 

```
MODE_15W_6CORE
2
```

Then make sure you switch your power mode to 15W with all 6 cores enables by running this command: 

```bash
sudo nvpmodel -m 2
```

## Setting up the Dockers for your Leo Rover

### Update Robot Description with your Leo Rover namespace

1. Navigate to:

```bash
cd ELYSIUM-XR-LeoRover-Dockers/leorover_description_zenoh_docker/ros2_ws/src/leo_description/urdf
```

And

```bash
cd ELYSIUM-XR-LeoRover-Dockers/leorover_description_zenoh_docker/ros2_ws/src/leo_description/launch
```

2. Edit this file (change leo04 to leoX) where X is your Leo Rover number

```bash
vim leo.urdf.xacro
vim state_publisher.launch.xml 
```

### Change Livox Configuration to match the LiDAR and Jetson used
 
1. See README for Livox Lidar docker (change MID360_config)
2. Change Launch file for MID360

```bash
cd /home/spacer/LeoRover-Docker-Containers/ELYSIUM-XR-LeoRover-Dockers/livox_docker_zenoh/ros2_ws/src/livox_ros_driver2/launchROS2/
vim MID360_launch.py
```

Change frame_id to the one for your Leo Rover (for example if using Leo08 -> 'leo08/livox_frame')


### Change Zenoh to Fast DDS cmd_vel topic

1. Go to the entrypoint.sh and change the parameter `--topic` to the `cmd_vel` topic corresponding to you robot




