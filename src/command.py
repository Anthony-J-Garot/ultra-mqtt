import os
# Project imports
from utils import log
import utils

def command_add_1gb_file(payload):
    log(f"CMD> Adding 1GB File. payload {payload}")
    name = "gig1"
    os.system(f"fallocate -l 1000M {name}.out")


def command_rm_1gb_file(payload):
    log(f"CMD> Removing 1GB File. payload {payload}")
    os.system("rm *.out")


def command_change_send_interval(payload):
    log(f"CMD> payload {payload}")
    new_interval = int(payload)

    # Less than 10s doesn't make much sense since graphing
    # on Losant seems to be limited to 10s
    if new_interval < 10:
        new_interval = 10

    utils.repeat_timer.update_interval(new_interval)


switcher = {
    "add_1gb_file": command_add_1gb_file,
    "rm_1gb_file": command_rm_1gb_file,
    "change_send_interval": command_change_send_interval
}
