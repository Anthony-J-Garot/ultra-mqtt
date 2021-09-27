#!/bin/bash

# Simpler runner script for the client

PYTHON=/usr/bin/python3

# This gets the secret into ACCESS_SECRET
source .secret.sh

CMD="$PYTHON src/ultra_mqtt_client.py $ACCESS_SECRET"
# echo $CMD
eval $CMD 
