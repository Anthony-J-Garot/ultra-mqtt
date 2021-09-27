"""
Adapted from the script
https://docs.losant.com/mqtt/python/
Repo: https://github.com/Losant/losant-mqtt-python

NOTE: The Keepalive is < 22 seconds from connection time
"""
import time
import sys
import os
from losantmqtt import Device

import repeat_timer
from utils import log
import device_wrap

# Constants
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


def main():
    # Listen for commands.
    device.add_event_observer("command", device_wrap.on_command)

    # Connect to Losant.
    log("Connecting to Losant")
    try:
        device.connect(blocking=False)
    except ConnectionRefusedError as e:
        log(f"Connection Refused: {e}")
        sys.exit(1)
    except Exception as e:
        log(f"Could not connect: {e}")
        sys.exit(1)
    time.sleep(KEEP_ALIVE)  # Give just a little time to actually connect

    # Create a timer
    log(f"Creating {SEND_INTERVAL}s repeat timer")
    repeat_timer.send_state_timer = repeat_timer.RepeatTimer.create(SEND_INTERVAL, device_wrap.send_space_usage, device)
    repeat_timer.send_state_timer.start()

    log("Starting infinite loop")
    not_connected_count = 0
    while not is_stopped:
        # Loops the network stack for the connection.
        # Only valid in non-blocking mode.
        device.loop(timeout=1)

        # The keepalive max is about 24 seconds for my location.
        time.sleep(KEEP_ALIVE)

        # So far, this hasn't been needed. There doesn't appear
        # to be a way to disconnect from the Losant site. I suppose
        # I could unplug an Ethernet cable . . . .
        if not device.is_connected():
            not_connected_count += 1
            if not_connected_count > 1:
                log(f"Device not connected. not_connected_count [{not_connected_count}]")


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
