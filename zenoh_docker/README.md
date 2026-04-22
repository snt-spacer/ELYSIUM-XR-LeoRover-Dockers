# Zenoh Router Docker

## Description
This repostory contains the files to build a Docker image that starts a Zenoh router such that the other docker containers on the Leo Rover can publish and subscribe to ROS 2 topics. The Docker used in this branch covers ROS 2 Jazzy is based on the Zenoh ROS2 Middleware `zenoh_rmw_cpp`.


# Getting started
Simply clone the parent git repository:

```bash
git clone https://github.com/snt-spacer/ELYSIUM-XR-LeoRover-Dockers.git
```

Then, enter the `docker` directory:

```bash
cd zenoh_docker/docker/
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
This repository contains two main directories, one called `docker` and one called `ros2_ws`. The `docker` directory contains the scripts mentioned above, to build the Docker image and to run, stop and test the Docker container. Additionally, this directory contains the `Dockerfile`, the recipe for the Docker image and the `entrypoint.sh` file. The entrypoint sources ROS 2, changes the communication middleware to `rmw_zenoh_cpp` and starts a `zenoh` router. 

**Note:** For changes in the file `entrypoint.sh`, the Docker image needs to be rebuilt as it is copied into the image and not mounted when running the container.

## Setting ROS environmental variables

The Docker container will take over the environmental variables of the host system for the `ROS_DOMAIN_ID`, the `ROS_NAMESPACE` and for the `ROS_LOCALHOST_ONLY` settings. This way, the `ROS_DOMAIN_ID` can easily be changed if needed for certain experiments and the `ROS_NAMESPACE` can be globally set for a robot and does not need to be adapted inside this repository, allowing for easily deploying the exact same repository on different robots with different namespaces and domain IDs without additional configuration by the user.