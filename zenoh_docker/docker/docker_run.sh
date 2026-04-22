#!/usr/bin/env bash

if [ ${#} -lt 1 ]; then
    #echo "Usage: ${0} <docker image> <cmd (optional)>"
    #exit 1
    IMG="local/zenohrouter:jazzy"
    CMD="source /entrypoint.sh"
fi


DOCKER_RUN_CMD=(
    docker run
    --interactive
    --tty
    --name "zenoh_router"
    # --network=bridge
    --network host
    --rm
    --ipc host
    -d
    --privileged
    --security-opt "seccomp=unconfined"
    --volume "/etc/localtime:/etc/localtime:ro"
    --volume "/dev:/dev"
    --volume "/dev/shm:/dev/shm"
    --volume "${PWD}/../zenoh_config/:/home/leo/zenoh_config/"
    --env ROS_NAMESPACE=${ROS_NAMESPACE}
    --env ROS_DOMAIN_ID=${ROS_DOMAIN_ID}
    --env ROS_LOCALHOST_ONLY=${ROS_LOCALHOST_ONLY}
    "${ENVS}"
    "${IMG}"
    #"${CMD}"
)

echo -e "\033[1;30m${DOCKER_RUN_CMD[*]}\033[0m" | xargs

# shellcheck disable=SC2048
exec ${DOCKER_RUN_CMD[*]}
