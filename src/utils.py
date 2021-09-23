from datetime import datetime
from threading import Timer

repeat_timer = None


# Decide when to send data
# https://stackoverflow.com/a/48741004/4171820
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

    def update_interval(self, new_interval):
        self.interval = new_interval


# Nice log output
def log(msg):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"{current_time}> {msg}")


def new_timer(duration, fn):
    global repeat_timer

    log(f"Creating new timer for {duration}s")
    repeat_timer = RepeatTimer(duration, fn)
    repeat_timer.start()
