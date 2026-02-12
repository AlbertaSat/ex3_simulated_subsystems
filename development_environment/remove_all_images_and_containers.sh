#!/bin/bash

#This is a script to remove all images and containers in case too many docker images are created locally.

echo "-----------------------------------!!!WARNING!!!-----------------------------------"
echo "THIS WILL DELETE ALL LOCAL IMAGES AND CONTAINERS!"
echo "IF YOU DO NOT WANT TO LOSE PROGRESS PLEASE COMMIT THE CHANGES INSIDE THE CONTAINER"
echo "Y/N: "

while true; do
    read -rsn1 key
    case $key in
        y|Y)
            docker image prune
            docker container prune
            exit 0
            ;;
        n|N)
            exit 0
            ;;
        *)
            echo "Please enter a 'Y' or 'N': "
            ;;
    esac
        done
