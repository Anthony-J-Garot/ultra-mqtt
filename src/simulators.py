"""
Device handlers and such.
"""
import secrets
import shutil

from losantmqtt import Device
import repeat_timer
import utils
from utils import log, wrap_send_state
from command import switcher

# Constants
SPACE_TOTAL = 0
SPACE_USED = 1
SPACE_FREE = 2
LOWER_BOUND = 0.000
UPPER_BOUND = 28.910  # Based upon my VM size
MAX_WALK = 1.000  # Maximum/Minimum (+/-) for random walk in GB.

# Module globals
used_hold = None
free_hold = None
secretsGenerator = secrets.SystemRandom()


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


def space_usage(device):
    """
This sends the hard drive space usage data to the Losant device.
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
    used = round(memory[SPACE_USED] / (2 ** 30), 3)
    free = round(memory[SPACE_FREE] / (2 ** 30), 3)
    total = round(memory[SPACE_TOTAL] / (2 ** 30), 3)
    # For client logging
    log(f"Device State: Used [{used} GB] Free [{free} GB] (of [{total} GB])")

    # Send attributes to Losant.
    # Note: you can send multiple states, but it's probably better to send
    # just a single payload of attributes. Attributes from separate states
    # are sometimes (not always) combined on the Losant side anyway.
    payload = {
        "drive-space-used": used,
        "drive-space-free": free
    }

    return wrap_send_state(device, payload)


def random_scatter(device):
    """
This sends random data to the Losant device. Is this useful? Perhaps not.
But this function sends floating point values, which the Losant Simulator
cannot do.
    """
    global is_stopped
    if not device.is_connected():
        log("Device not connected. Turning off timer")
        repeat_timer.send_state_timer.cancel()
        is_stopped = True
        return False

    # Convert into GB
    secretsGenerator.seed()
    used = round(secretsGenerator.uniform(LOWER_BOUND, UPPER_BOUND), 3)
    total = UPPER_BOUND
    free = round(total - used, 3)
    # For client logging
    log(f"Device State: Used [{used} GB] Free [{free} GB] (of [{total} GB])")

    # Send attributes to Losant.
    # Note: you can send multiple states, but it's probably better to send
    # just a single payload of attributes. Attributes from separate states
    # are sometimes (not always) combined on the Losant side anyway.
    payload = {
        "drive-space-used": used,
        "drive-space-free": free
    }

    return wrap_send_state(device, payload)


def random_walk(device):
    """
Random data isn't very interesting because it's just all over the place.
This adds or subtracts a random amount from the current value, which better
emulates what a hard drive would probably do.
    """
    global is_stopped, used_hold
    if not device.is_connected():
        log("Device not connected. Turning off timer")
        repeat_timer.send_state_timer.cancel()
        is_stopped = True
        return False

    # Set default hold values
    if used_hold is None:
        # Initialize to actual hard drive value
        memory = shutil.disk_usage("/")
        used_hold = round(memory[SPACE_USED] / (2 ** 30), 3)
        free_hold = round(UPPER_BOUND - used_hold, 3)

    # Convert into GB
    secretsGenerator.seed()
    walk = secretsGenerator.uniform(-MAX_WALK, MAX_WALK)
    used = round(used_hold + walk, 3)
    used = min(used, UPPER_BOUND)
    used = max(used, LOWER_BOUND)
    # print(f"walk {walk} used {used}")
    total = UPPER_BOUND
    free = round(total - used, 3)
    # For client logging
    log(f"Device State: Used [{used} GB] Free [{free} GB] (of [{total} GB])")

    # Send attributes to Losant.
    # Note: you can send multiple states, but it's probably better to send
    # just a single payload of attributes. Attributes from separate states
    # are sometimes (not always) combined on the Losant side anyway.
    payload = {
        "drive-space-used": used,
        "drive-space-free": free
    }

    LOW_POWER = True  # For now, just a simple switch. Not sure how I will tie this in.
    # For convenience, the MAX_DEVIATION is set to 80% of the MAX_WALK. This
    # would be a user-set value based upon expected values. For example, if
    # a temperature probe may be accurate to .01 degrees, but anything under a
    # full 1.00 degree change may just be considered noise.
    MAX_DEVIATION = MAX_WALK * .80  # allowed deviation before reporting
    if LOW_POWER:
        deviation = utils.drive_space_deviation(used, used_hold)
        if deviation > MAX_DEVIATION:
            log(f"deviation [{deviation}] > [{MAX_DEVIATION}] . . . sending message to Broker.")
            if not wrap_send_state(device, payload):
                return False
            # Update hold values only if reported
            used_hold = used
            free_hold = free
        else:
            log(f"deviation [{deviation}] NOT > [{MAX_DEVIATION}] . . . so, NOT sending to Broker.")

        return True
    else:
        # Keep track of hold values
        used_hold = used
        free_hold = free

        return wrap_send_state(device, payload)


dispatcher = {
    "space_usage": space_usage,
    "random_walk": random_walk,
    "random_scatter": random_scatter
}
