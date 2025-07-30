#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Time taking.

Mostly for measurements of nexium of itself, e.g. how long did it take to
call an external tool.
"""

from timeit import default_timer as timer

from qutayba.Tracing import general


class StopWatch(object):
    __slots__ = ("start_time", "end_time")

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = timer()

    def restart(self):
        self.start()

    def end(self):
        self.end_time = timer()

    stop = end

    def getDelta(self):
        if self.end_time is not None:
            return self.end_time - self.start_time
        else:
            return timer() - self.start_time


class TimerReport(object):
    """Timer that reports how long things took.

    Mostly intended as a wrapper for external process calls.
    """

    __slots__ = ("message", "decider", "logger", "timer", "min_report_time")

    def __init__(self, message, logger=None, decider=True, min_report_time=None):
        self.message = message

        # Shortcuts.
        if decider is True:
            decider = lambda: 1
        elif decider is False:
            decider = lambda: 0

        if logger is None:
            logger = general

        self.logger = logger
        self.decider = decider
        self.min_report_time = min_report_time

        self.timer = None

    def getTimer(self):
        return self.timer

    def __enter__(self):
        self.timer = StopWatch()
        self.timer.start()

        return self.timer

    def __exit__(self, exception_type, exception_value, exception_tb):
        self.timer.end()

        delta_time = self.timer.getDelta()

        # Check if its above the provided limit.
        above_threshold = (
            self.min_report_time is None or delta_time >= self.min_report_time
        )

        if exception_type is None and above_threshold and self.decider():
            self.logger.info(self.message % self.timer.getDelta(), keep_format=True)



