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

# Start the leorover description
ros2 launch leo_description state_publisher.launch.xml

exec "$@"
