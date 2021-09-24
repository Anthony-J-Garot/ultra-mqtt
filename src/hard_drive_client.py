"""
Adapted from the script
https://docs.losant.com/mqtt/python/
Repo: https://github.com/Losant/losant-mqtt-python

NOTE: The Keepalive is < 22 seconds from connection time
"""
import time
import shutil
import sys
import os
from losantmqtt import Device

import repeat_timer
from command import switcher
from utils import log

# Constants
SPACE_TOTAL = 0
SPACE_USED = 1
SPACE_FREE = 2
KEEP_ALIVE = 1
# Send hard drive disk space once every SEND_INTERVAL seconds.
# There doesn't seem to be much use of having this < 10 seconds since
# Losant charting only goes down to 10s granularity.
# SEND_INTERVAL = 5 * 60
SEND_INTERVAL = 10

# Globals
is_stopped = False

# Idiot check
if len(sys.argv) != 2:
    print("You must pass in the Access Secret")
    sys.exit(1)

# Construct device from stuff we know and secret
device = Device(
    "614b9487f397de0006ba4c21",
    "070c3950-c1e4-4c89-b030-0832441c79fd",
    sys.argv[1]
)


def on_command(device, command):
    """
Receives triggers from Losant, e.g. push-buttons.
The first argument for all callbacks is the device instance.
The second is a Dict with a name and payload.
    """

    # The Dict has some interesting stuff like the deviceid, key, secret
    # and a few other settings. Not sure any of that is useful here, but
    # I dumped it to the screen to remind me it's available.
    print(f"MQTT endpoint [{device.mqtt_endpoint}]")
    print(f"dict [{device.__dict__}]")

    # These are useful for debugging, but noisy for general use
    if True:
        log("Command received from Losant MQTT broker.")
        log(command["name"])
        log(command["payload"])
    switcher[command["name"]](command["payload"])


# This sends the actual data to the device
def send_space_usage():
    global is_stopped
    if not device.is_connected():
        log("Device not connected. Turning off timer")
        repeat_timer.send_state_timer.cancel()
        is_stopped = True
        return

    # Get the hard drive space usage
    # total, used, free = shutil.disk_usage("/")
    memory = shutil.disk_usage("/")
    # Convert into GB
    used = int((memory[SPACE_USED] / (2 ** 30)) * 1000) / 1000
    free = int((memory[SPACE_FREE] / (2 ** 30)) * 1000) / 1000
    # For client logging
    log(f"Used: {used} Free: {free}")

    # Send attributes to Losant.
    # Note: you can send multiple states, but it's probably better to send
    # just a single payload of attributes. Attributes from separate states
    # are sometimes (not always) combined on the Losant side anyway.
    payload = {
        "drive-space-used": used,
        "drive-space-free": free
    }
    device.send_state(payload)


def main():
    # Listen for commands.
    device.add_event_observer("command", on_command)

    # Connect to Losant.
    device.connect(blocking=False)

    # Create a timer
    repeat_timer.send_state_timer = repeat_timer.RepeatTimer.create(SEND_INTERVAL, send_space_usage)
    repeat_timer.send_state_timer.start()

    log("Starting infinite loop")
    while not is_stopped:
        # Loops the network stack for the connection.
        # Only valid in non-blocking mode.
        device.loop(timeout=1)

        # The keepalive max is about 24 seconds.
        time.sleep(KEEP_ALIVE)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')

        is_stopped = True
        repeat_timer.send_state_timer.cancel()

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(os.EX_OK)
