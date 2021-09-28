#!/bin/bash

# Simpler runner script for the client

PYTHON=/usr/bin/python3

# This gets the secret into ACCESS_SECRET
source .secret.sh

# Build the command.
# NOTE: $1 allows for a different data send function, e.g. "random_scatter"
CMD="$PYTHON src/ultra_mqtt_client.py $ACCESS_SECRET $1"
# echo $CMD
eval $CMD 
