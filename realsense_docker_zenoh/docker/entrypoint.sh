#!/bin/bash

set -e

export ROS2_INSTALL_PATH="/opt/ros/${ROS_DISTRO}"
export ROS_NAMESPACE=${ROS_NAMESPACE}
export ROS_DOMAIN_ID=${ROS_DOMAIN_ID}

# setup ros2 environment
cd /home/leo/ros2_ws
source "/opt/ros/${ROS_DISTRO}/setup.bash"
colcon build
source "/home/leo/ros2_ws/install/setup.bash"

# setup zenoh configuration
pkill -9 -f ros && ros2 daemon stop
export RMW_IMPLEMENTATION=rmw_zenoh_cpp

# Start Realsense Camerar
ros2 launch leorover_realsense ns_d455_launch.py


exec "$@"
