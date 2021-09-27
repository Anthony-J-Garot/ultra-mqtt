#!/bin/sh

# A handy little sh script to put on your router. Why sh instead of bash?
# FreshTomato doesn't have bash. :/
#
# This script intercepts traffic to the Losant Broker and directs it to your
# own broker.
#
# To find the LOSANT_BROKER IP address, connect with your client, then run:
#
#    $ sudo lsof -i -P -n | grep ":8883"
#

MQTT_CLIENT=192.168.2.99 # My local VM
VM=192.168.2.99          # My local VM
LOSANT_BROKER=0.0.0.0    # Masking Losant's IP. See above on how to find it.
PORT=8883                # SSL version

case $1 in
capture)
    iptables -t nat \
        -I PREROUTING \
        -p tcp \
        -s $MQTT_CLIENT \
        -d $LOSANT_BROKER \
        --dport $PORT \
        -j DNAT --to $VM:$PORT

    iptables -t nat --list
    ;;
uncapture)
    iptables -t nat \
        -D PREROUTING \
        -p tcp \
        -s $MQTT_CLIENT \
        -d $LOSANT_BROKER \
        --dport $PORT \
        -j DNAT --to $VM:$PORT

    iptables -t nat --list
    ;;
*)
    echo "Nothing to do. Specify capture or uncapture."
    ;;
esac
