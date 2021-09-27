"""
Device handlers and such.
"""
import shutil
from losantmqtt import Device
import repeat_timer
from utils import log
from command import switcher

# Constants
SPACE_TOTAL = 0
SPACE_USED = 1
SPACE_FREE = 2


def create_device(device_id, key, secret):
    """
Wraps around the Losant Device() constructor.
    """
    return Device(device_id, key, secret)


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

    log(f"Command received from Losant MQTT broker {command['name']}.")
    # log(command["payload"])
    switcher[command["name"]](command["payload"])


def send_space_usage(device):
    """
This sends the actual data to the device.
    """
    global is_stopped
    if not device.is_connected():
        log("Device not connected. Turning off timer")
        repeat_timer.send_state_timer.cancel()
        is_stopped = True
        return False

    # Get the hard drive space usage
    # total, used, free = shutil.disk_usage("/")
    memory = shutil.disk_usage("/")
    # Convert into GB
    used = int((memory[SPACE_USED] / (2 ** 30)) * 1000) / 1000
    free = int((memory[SPACE_FREE] / (2 ** 30)) * 1000) / 1000
    total = int((memory[SPACE_TOTAL] / (2 ** 30)) * 1000) / 1000
    # For client logging
    log(f"Device State: Used [{used}GB] Free [{free}GB] (of [{total}GB])")

    # Send attributes to Losant.
    # Note: you can send multiple states, but it's probably better to send
    # just a single payload of attributes. Attributes from separate states
    # are sometimes (not always) combined on the Losant side anyway.
    payload = {
        "drive-space-used": used,
        "drive-space-free": free
    }

    try:
        device.send_state(payload)
    except Exception as error:
        log(f"Could not send_state: {error}")
        return False

    return True
