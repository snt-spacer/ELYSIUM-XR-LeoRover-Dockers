ARG PARENT_IMAGE=ros
ARG PARENT_TAG=humble
FROM ${PARENT_IMAGE}:${PARENT_TAG}

# RUN useradd -ms /bin/bash leo

### Use bash by default
SHELL ["/bin/bash", "-c"]

### Set non-interactive installation
ARG DEBIAN_FRONTEND=noninteractive


### Install realsense2-camera
RUN apt-get update && \
    apt-get install -yq vim && \
    apt-get install -yq --no-install-recommends \
    "ros-${ROS_DISTRO}-realsense2-camera" && \
    apt-get install -yq python3-colcon-common-extensions && \
    rm -rf /var/lib/apt/lists/*

# Install Zenoh RMW
RUN apt update && apt install -y \
ros-${ROS_DISTRO}-rmw-zenoh-cpp && \
rm -rf /var/lib/apt/lists/*

### Copy over config files and launch scripts
# COPY ./config ${WS_DIR}/config
COPY ./config /home/leo/config
# COPY ./launch ${WS_DIR}/launch
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
# RUN chmod +x /launch/lunalab_leo03.bash
ENTRYPOINT ["/entrypoint.sh"]

# USER leo
WORKDIR /home/leo

# RUN mkdir -p /home/leo/ros2_ws/src
### Set default command

CMD ["bash"]

#CMD ["launch/lunalab_summit_xl_gen.bash"]
