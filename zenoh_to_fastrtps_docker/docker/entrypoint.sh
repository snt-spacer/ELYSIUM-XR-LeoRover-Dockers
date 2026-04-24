#!/bin/bash

set -e

export ROS2_INSTALL_PATH="/opt/ros/${ROS_DISTRO}"


export ROS_NAMESPACE=${ROS_NAMESPACE}
export ROS_DOMAIN_ID=${ROS_DOMAIN_ID}

# kill ROS2 Process and any fast-DDS interference
pkill -9 -f ros && ros2 daemon stop


# setup ros2 environment
source "/opt/ros/${ROS_DISTRO}/setup.bash"


(
 export RMW_IMPLEMENTATION=rmw_zenoh_cpp
 export ROS_DOMAIN_ID="${ROS_DOMAIN_ID}"
 exec python3 /home/leo/relays/cmdvel_zenohtx.py
) & Z2U_PID=$!

(
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID}"
exec python3 /home/leo/relays/cmdvel_fastrx.py
) & U2F_PID=$!




exec "$@"
