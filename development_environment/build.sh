#!/bin/bash


#This should work if you have ssh-keys set up correctly using an ssh agent
#If this doesn't work then you can run the following commands:
#eval ssh-agent $SHELL
#ssh-add <path/to/private-github-access-key>

export DOCKER_BUILDKIT=1
docker build -t environment --build-arg "UID=$(id -u)" --build-arg "GID=$(id -g)" --ssh default .
