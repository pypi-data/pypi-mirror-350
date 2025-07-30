#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Threaded pool execution.

This can use Python3 native, or even Python2.7 backport, or has a Python2.6
stub that does not thread at all.
"""

from threading import RLock, current_thread

# Set this to false, to enable actual use of threads. This was found no longer
# useful with dependency walker, but might be true in other cases.
_use_threaded_executor = False


class NonThreadedPoolExecutor(object):
    def __init__(self, max_workers=None):
        # This stub ignores max_workers, pylint: disable=unused-argument

        self.results = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return False

    def submit(self, function, *args):
        # Submitted jobs are simply done immediately.
        self.results.append(function(*args))

        return self


def waitWorkers(workers):
    if workers:
        return iter(workers[0].results)


ThreadPoolExecutor = NonThreadedPoolExecutor


if _use_threaded_executor:
    try:
        from concurrent.futures import (  # pylint: disable=I0021,import-error,no-name-in-module,unused-import
            FIRST_EXCEPTION,
            ThreadPoolExecutor,
            as_completed,
            wait,
        )

        # We overwrite this if wanted, pylint: disable=function-redefined
        def waitWorkers(workers):
            wait(workers, return_when=FIRST_EXCEPTION)

            for future in as_completed(workers):
                yield future.result()

    except ImportError:
        # No backport installed, use stub for at least Python 2.6, and potentially
        # also Python 2.7, we might want to tell the user about it though, that
        # we think it should be installed.
        pass


def getThreadIdent():
    return current_thread()


assert RLock
assert ThreadPoolExecutor


