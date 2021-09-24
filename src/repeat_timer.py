from threading import Timer
from utils import log

send_state_timer = None


# Decide when to send data
# https://stackoverflow.com/a/48741004/4171820
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

    def update_interval(self, new_interval):
        """
Updates the repeat_timer's interval.
        """
        # Less than 10s doesn't make much sense since graphing on Losant seems to be limited to 10s
        new_interval = max(new_interval, 10)
        self.interval = new_interval

    @staticmethod
    def create(duration, callback_fn):
        """
Creates a timer based upon threading's Timer.
Sends periodic data w/o upsetting the keepalive loop.
        """
        log(f"Creating new timer for {duration}s")
        return RepeatTimer(duration, callback_fn)
