#!/bin/bash

CONTAINER_NAME="leo_realsense"

# Check if the 'leo_realsense' container is running
if docker inspect -f '{{.State.Running}}' ${CONTAINER_NAME} &>/dev/null; then
    # Execute your commands here
    echo "Container '${CONTAINER_NAME}' is running."
    echo -n "Stopping container: "
    docker stop ${CONTAINER_NAME}
    echo -n "Removing container: "
    docker rm ${CONTAINER_NAME}
else
    echo "Container '${CONTAINER_NAME}' is not running."
fi
