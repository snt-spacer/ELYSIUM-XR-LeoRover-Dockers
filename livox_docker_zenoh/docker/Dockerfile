# Use the official ROS2 image as the base image
FROM ros:jazzy-ros-base
LABEL maintainer="Alexandre Frantz <alexandre.frantz@uni.lu>"


## Use bash by default
SHELL ["/bin/bash", "-c"]


## Set non-iteractive installation
ARG DEBIAN_FRONTEND=noninteractive


# Install ROS2 packages
RUN apt update && \
apt install -y \
ros-${ROS_DISTRO}-pcl-ros \
ros-${ROS_DISTRO}-rviz2 \
python3-colcon-common-extensions && \
rm -rf /var/lib/apt/lists/*

# Install Zenoh RMW
RUN apt update && apt install -y \
ros-${ROS_DISTRO}-rmw-zenoh-cpp && \
rm -rf /var/lib/apt/lists/*
# last line to remove unecessary stuff
# and reduce image size



## Copy over config files
RUN mkdir /home/leo
COPY ./config /home/leo/config


# Set up entrypoint to source ROS2 setup files
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]


RUN mkdir -p /root/ros2_ws/src/

# Set the default command to run when the container starts
CMD ["bash"]
