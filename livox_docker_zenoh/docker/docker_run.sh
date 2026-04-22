#!/bin/bash
#xhost +local:docker
LEOROVER='leo04'

# Note: replace --restart=always to --rm for testing
docker run -it \
    -d \
    --interactive \
    --rm \
    --network=host \
    --ipc=host \
    --privileged \
    --env ROS_NAMESPACE=${ROS_NAMESPACE} \
    --env ROS_DOMAIN_ID=${ROS_DOMAIN_ID} \
    --security-opt="seccomp=unconfined" \
    --volume="${PWD}/../ros2_ws/src/livox_ros_driver2:/root/ros2_ws/src/livox_ros_driver2" \
    --volume="${PWD}/../Livox-SDK2/:/root/Livox-SDK2" \
    --volume="/etc/localtime:/etc/localtime:ro" \
    --volume="/dev/shm:/dev/shm" \
    --name mid_360_zenoh \
    local/mid_360_zenoh:jazzy \
    #ros2 launch livox_ros_driver2 MID360_main_launch.py   
    #ros2 launch livox_ros_driver2 rviz_MID360_launch.py
