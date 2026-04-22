# realsense_docker

## Description
This repostory contains the files to build a Docker image that contains the default ROS 2 package for the Realsense Camera. It currently uses the default `ros2_ws` of the robot to launch the `realsense_camera` ROS 2 package. The Docker used in this branch covers ROS 2 Humble.


## Getting started
Simply clone this git repository:

```bash
git clone https://github.com/Dave-van-der-Meer/realsense_docker.git
```

Then, enter the `docker` directory:

```bash
cd realsense_docker/docker/
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
- If you want to test the Docker container by logging into an interactive bash shell, use the script `docker_test.sh`.


## Project structure
This repository contains two main directories, one called `docker` and one called `ros2_ws`. The `docker` directory contains the scripts mentioned above, to build the Docker image and to run, stop and test the Docker container. Additionally, this directory contains the `Dockerfile`, the recipe for the Docker image and the `entrypoint.sh` file. The entrypoint sources ROS 2 and builds the ROS workspace inside the container, called `ros2_ws`.

The `ros2_ws` directory can be used as a standalone ROS 2 workspace. In combination with Docker, it will be mounted as a volume so that the container has access to the content of the source code in the `ros2_ws/src` directory. Upon starting the container, this source code will be compiled and the indicated launch file will be run.

The reason, the `ros2_ws` is mounted only when running the container is to allow modifying the launch configuration inside the ROS 2 launch file, outside of the container. As a result, it is easily possible to modify the camera parameters without the need to rebuild the Docker image and copy the launch files into the image.

To allow the Docker container to communicate with the host machine and with remote devices, the file `docker/config/fastrtps-profile.xml` changes the DDS settings accordingly. Therefore, the system memory will be made accessible when running the container by usong the flags `--network host --ipc host --volume "/dev/shm:/dev/shm"`. They allow for the Docker container to communicate with other ROS 2 nodes as if it was running directly on the host.

**Note:** For changes in the file `entrypoint.sh`, the Docker image needs to be rebuilt as it is copied into the image and not mounted when running the container.


## Setting ROS environmental variables

The Docker container will take over the environmental variables of the host system for the `ROS_DOMAIN_ID`, the `ROS_NAMESPACE` and for the `ROS_LOCALHOST_ONLY` settings. This way, the `ROS_DOMAIN_ID` can easily be changed if needed for certain experiments and the `ROS_NAMESPACE` can be globally set for a robot and does not need to be adapted inside this repository, allowing for easily deploying the exact same repository on different robots with different namespaces and domain IDs without additional configuration by the user.