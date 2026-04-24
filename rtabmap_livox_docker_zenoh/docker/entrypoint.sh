#!/bin/bash

set -e

export ROS2_INSTALL_PATH="/opt/ros/${ROS_DISTRO}"
export ROS_NAMESPACE=${ROS_NAMESPACE}
export ROS_DOMAIN_ID=${ROS_DOMAIN_ID}

# kill ROS2 Process and any fast-DDS interference
pkill -9 -f ros && ros2 daemon stop

# Configure DDS
export RMW_IMPLEMENTATION=rmw_zenoh_cpp

# setup ros2 environment
cd /home/leo/ros2_ws
source "/opt/ros/${ROS_DISTRO}/setup.bash"
colcon build
source "/home/leo/ros2_ws/install/setup.bash"

# Start RTABMAP
# (
# ros2 launch rtabmap_livox rtabmap_livox_projection.launch.py
# ) & RTB_PID=$!

# Start Nav2
#(
#ros2 launch rtabmap_livox custom_nav.launch.py params_file:=/home/leo/nav2_params_repo.yaml # Original

#ros2 launch rtabmap_livox custom_nav.launch.py params_file:=/home/leo/nav2_params_repo_testing.yaml
#) & NAV_PID=$!


# Bridge DDS topics (testing)
# export ZENOH_CONFIG_OVERRIDE='mode="client";connect/endpoints=["192.168.88.102"];plugins/ros2dds/__required__=true;plugins/ros2dds/domain=4;plugins/ros2dds/namespace="/leo04"'
# ros2 run rmw_zenoh_cpp rmw_zenohd
# zenoh-bridge-ros2dds

exec "$@"
