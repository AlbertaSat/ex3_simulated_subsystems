#!/bin/bash


git init ~/ex3_simulated_subsystems/

message=""
branch=""

echo -e "Make sure you have switched to the correct branch!\n"


read -p "Please enter your commit message: " ${message}

git add .

git commit -m "${message}"
git push
