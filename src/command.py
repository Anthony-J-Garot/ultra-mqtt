"""
All triggers from Losant to the client are described herein.
"""
import os
import repeat_timer
from utils import log


def command_add_1gb_file(payload):
    """
Creates a 1GB file on the local hard drive. This will
change both the used and free values during the next
poll cycle.
    """
    log(f"CMD> Adding 1GB File. payload {payload}")
    name = "gig1"
    os.system(f"fallocate -l 1000M {name}.out")


def command_rm_1gb_file(payload):
    """
Delete the 1GB file on the local hard drive.
    """
    log(f"CMD> Removing 1GB File. payload {payload}")
    os.system("rm *.out")


def command_change_send_interval(payload):
    """
The dashboard contains a text field and push-button that changes the
send interval on the client.

At present, the payload is just a string value, not JSON. At present,
that is enough.
    """
    log(f"CMD> payload [{payload}]")
    new_interval = int(payload)

    if repeat_timer.send_state_timer is None:
        log("No access to the repeat timer. Cannot change the interval.")
        return

    repeat_timer.send_state_timer.update_interval(new_interval)


switcher = {
    "add_1gb_file": command_add_1gb_file,
    "rm_1gb_file": command_rm_1gb_file,
    "change_send_interval": command_change_send_interval
}
