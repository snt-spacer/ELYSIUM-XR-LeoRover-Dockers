ARG PARENT_IMAGE=ros
ARG PARENT_TAG=jazzy
FROM ${PARENT_IMAGE}:${PARENT_TAG}

# RUN useradd -ms /bin/bash leo

### Use bash by default
SHELL ["/bin/bash", "-c"]

### Set non-interactive installation
ARG DEBIAN_FRONTEND=noninteractive


### Install vim
RUN apt-get update && \
    apt-get install -yq vim

### Install Nav2
RUN apt-get update && \
    apt-get install -yq ros-jazzy-navigation2 && \
    apt-get install -yq ros-jazzy-nav2-bringup


### Install RTABMAP
RUN apt-get update && \
    apt-get install -yq ros-jazzy-rtabmap-ros

### Install zenoh RMW 
RUN apt-get install -yq ros-jazzy-rmw-zenoh-cpp

### Install zenoh ros2DDS bridge
RUN echo "deb [trusted=yes] https://download.eclipse.org/zenoh/debian-repo/ /" | sudo tee -a /etc/apt/sources.list > /dev/null
RUN sudo apt-get update 

### Install demo nodes
RUN apt-get install -yq ros-jazzy-demo-nodes-cpp \
    ros-jazzy-xacro 

### Install colcon
RUN apt-get install -yq python3-colcon-common-extensions && \
    rm -rf /var/lib/apt/lists/*

### Copy over config files and launch scripts
COPY ./config /home/leo/config
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# USER leo
WORKDIR /home/leo

# RUN mkdir -p /home/leo/ros2_ws/src
### Set default command

CMD ["bash"]

#CMD ["launch/lunalab_summit_xl_gen.bash"]
