"""
General utilities used throughout the application.
"""
from datetime import datetime

# Good to the thousandths place. This is based upon hard drive space.
# For temperatures, we might be concerned with only hundredths or tenths
# of a degree, depending upon the precision of the probe.
drive_space_deviation = lambda x, hold_x: round(abs(x - hold_x), 3)


# Nicer log output
def log(msg, now=None):
    """
Owing that this is basically a print() replacement, this function is perhaps
more complex than it needs to be, but that is due, in part, to make it testable.
    """

    # Allow for a passed timestamp
    if now is None:
        now = datetime.now()
    formatted_time = now.strftime("%H:%M:%S")
    full_msg = f"{formatted_time}> {msg}"
    # Send it to stdout for now.
    print(full_msg)
    # Return it for testability
    return full_msg


def wrap_send_state(device, payload):
    """
Wrapper to the losantmqtt send_state() function.
Returns boolean.
    """
    try:
        device.send_state(payload)
    except Exception as error:
        log(f"Could not send_state: {error}")
        return False

    return True
