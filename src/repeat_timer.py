"""
This module provides a "repeat timer" based upon threading. This allows the sending
of periodic data without interfering with the keepalive connection loop.
"""
from threading import Timer
from utils import log

send_state_timer = None


# https://stackoverflow.com/a/48741004/4171820
class RepeatTimer(Timer):
    """
Provides the repeat timer functionality.
    """

    def run(self):
        """
This is what causes the repeat.
        """
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

    def update_interval(self, new_interval):
        """
Updates the repeat_timer's interval.
        """
        # Less than 10s doesn't make much sense since graphing on Losant seems to be limited to 10s
        new_interval = max(new_interval, 10)
        log(f"Updated interval to [{new_interval}s]")
        self.interval = new_interval

    @staticmethod
    def create(duration, callback_fn, *args):
        """
Creates a timer based upon threading's Timer.
Sends periodic data w/o upsetting the keepalive loop.
        """
        return RepeatTimer(duration, callback_fn, args)
