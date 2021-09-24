from datetime import datetime

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
