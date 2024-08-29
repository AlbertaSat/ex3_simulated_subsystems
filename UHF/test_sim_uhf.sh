#!/bin/bash

# user must be in "ex3_simulated_subsystems/UHF" to run this script
required_dir="UHF"

# Get the basename of the current working directory
current_basename=$(basename "$PWD")

# Check if the current directory matches the required directory
if [ "$current_basename" != "$required_dir" ]; then
  echo "Error: This script must be run from the $required_dir directory."
  exit 1
fi

# Spawn terminal for simulated UHF
gnome-terminal --title="SIM_UHF" -- bash -c "echo 'Starting simulated UHF'; sleep 0.5; python3 simulated_uhf.py; exec bash"

# Spawn terminal for fake coms handler
gnome-terminal --title="COMS_HANDLER" -- bash -c "echo 'Starting simulated coms handler'; sleep 0.5; python3 generic_client.py 1805; exec bash"

# Spawn terminal for fake gs
gnome-terminal --title="GS" -- bash -c "echo 'Starting simulated gs'; sleep 0.5; python3 generic_client.py 1808; exec bash"

