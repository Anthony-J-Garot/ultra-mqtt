import time
from losantmqtt import Device
import shutil

import sys
import os
# Project imports
from command import switcher
from utils import log, new_timer
import utils

# Adapted from the script
# https://docs.losant.com/mqtt/python/
# Repo: https://github.com/Losant/losant-mqtt-python
#
# NOTE: The Keepalive is < 22 seconds from connection time

# Send hard drive disk space once every send_interval seconds.
# There doesn't seem to be much use of having this < 10 seconds since
# Losant charting only goes down to 10s granularity.
# send_interval = 5 * 60
send_interval = 30
is_stopped = False

# Idiot check
if len(sys.argv) != 2:
    print("You must pass in the Access Secret")
    exit(1)

# Construct device from stuff we know and secret
device = Device(
    "614b9487f397de0006ba4c21",
    "070c3950-c1e4-4c89-b030-0832441c79fd",
    sys.argv[1]
)


# Receives triggers from Losant, e.g. push-buttons
def on_command(device, command):
    # These are useful for debugging, but noisy for general use
    if True:
        log("Command received.")
        log(command["name"])
        log(command["payload"])
    switcher[command["name"]](command["payload"])


# This sends the actual data to the device
def send_space_usage():
    global is_stopped, device
    if not device.is_connected():
        log("Device not connected. Turning off timer")
        utils.repeat_timer.cancel()
        is_stopped = True
        return

    # Get the hard drive space usage
    total, used, free = shutil.disk_usage("/")
    # Convert into GB
    used = int((used / (2 ** 30)) * 1000) / 1000
    free = int((free / (2 ** 30)) * 1000) / 1000
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
    global device

    # Listen for commands.
    device.add_event_observer("command", on_command)

    # Connect to Losant.
    device.connect(blocking=False)

    # Create a timer
    new_timer(send_interval, send_space_usage)

    log("Starting infinite loop")
    while not is_stopped:
        # Loops the network stack for the connection.
        # Only valid in non-blocking mode.
        device.loop(timeout=1)

        # The keepalive is about 24 seconds.
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(os.EX_OK)
