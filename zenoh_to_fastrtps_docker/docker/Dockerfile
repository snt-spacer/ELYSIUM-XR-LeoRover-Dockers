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

### Install zenoh RMW 
RUN apt-get install -yq ros-jazzy-rmw-zenoh-cpp

### Install demo nodes
RUN apt-get install -yq ros-jazzy-demo-nodes-cpp

### Install colcon
RUN apt-get install -yq python3-colcon-common-extensions && \
    rm -rf /var/lib/apt/lists/*

### Copy over config files and launch scripts
COPY ./config /home/leo/config
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

### Copy Zenoh to Fast relay scripts
COPY ./relays/* /home/leo/relays/
RUN chmod +x /home/leo/relays/*

# USER leo
WORKDIR /home/leo

# RUN mkdir -p /home/leo/ros2_ws/src
### Set default command

CMD ["bash"]

#CMD ["launch/lunalab_summit_xl_gen.bash"]
