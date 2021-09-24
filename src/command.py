import os

import repeat_timer
from utils import log


def command_add_1gb_file(payload):
    log(f"CMD> Adding 1GB File. payload {payload}")
    name = "gig1"
    os.system(f"fallocate -l 1000M {name}.out")


def command_rm_1gb_file(payload):
    log(f"CMD> Removing 1GB File. payload {payload}")
    os.system("rm *.out")


def command_change_send_interval(payload):
    # At present, the payload it just a string value, not JSON.
    log(f"CMD> payload {payload}")
    new_interval = int(payload)

    if repeat_timer.send_state_timer is None:
        print("STILL DON'T HAVE IT")
        return

    repeat_timer.send_state_timer.update_interval(new_interval)


switcher = {
    "add_1gb_file": command_add_1gb_file,
    "rm_1gb_file": command_rm_1gb_file,
    "change_send_interval": command_change_send_interval
}
