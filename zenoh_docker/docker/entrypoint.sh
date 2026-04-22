#!/bin/bash

set -e

export ROS2_INSTALL_PATH="/opt/ros/${ROS_DISTRO}"

export ROS_NAMESPACE=${ROS_NAMESPACE}
export ROS_DOMAIN_ID=${ROS_DOMAIN_ID}

# kill ROS2 Process and any fast-DDS interference
pkill -9 -f ros && ros2 daemon stop

# Configure DDS
export RMW_IMPLEMENTATION=rmw_zenoh_cpp

export ZENOH_ROUTER_CONFIG_URI="/home/leo/zenoh_config/zenoh_config.json5"

source "/opt/ros/${ROS_DISTRO}/setup.bash"

# Start Zenoh Server
ros2 run rmw_zenoh_cpp rmw_zenohd

exec "$@"
