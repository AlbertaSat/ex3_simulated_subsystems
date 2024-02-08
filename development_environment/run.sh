#!/bin/bash

#This runs the docker container in interactive mode and provides a bash terminal to interact in.
#It also will restart a created container in interactive mode

homedir=$( getent passwd "$USER" | cut -d: -f6 )

if [ $( docker ps -a -f name=development_environment | wc -l ) -eq 2 ]; then
    docker start development_environment
    docker attach development_environment
else
    docker run -it --name development_environment --mount type=bind,source=${homedir}/.ssh,target=/app/.ssh \
    environment /bin/bash
fi
