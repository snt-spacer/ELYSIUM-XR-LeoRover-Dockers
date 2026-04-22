# ELYSIUM-XR LeoRover Dockers

## Description
This repository contains the docker containers to launch the Leo Rover with the inverted LiDAR configuration. The docker containers are based on ROS 2 Jazzy and use the `rmw_zenoh_cpp` ROS 2 middleware to communicate with each other. 

Inside this repo you will find the following docker containers:

- `livox_docker_zenoh`: contains the Livox MID 360 3D LiDAR docker to launch the sensor
- `zenoh_docker`: contains the Zenoh router configuration and launches a Zenoh router 
- `leorover_description_zenoh_docker`: contains the Leo Rover URDF description with the inverted mount for the Livox LiDAR 



## Launching the docker containers

To launch all the docker containers and essentially initialize your ROS 2 nodes to work with the Leo you must first start the Zenoh router on the rover

1. Remotely connect to the rover via `ssh`

```bash
ssh <username>@<robot_ip>
```

2. Create a folder in side the `home` directory and clone the repo

```bash 
mkdir LeoRover-Dockers
git clone https://github.com/snt-spacer/ELYSIUM-XR-LeoRover-Dockers.git
```

3. Navigate to each docker container and launch them (see README.md for each docker container)



