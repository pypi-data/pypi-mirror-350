#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Progress bar for Scons compilation part.

This does only the interfacing with tracing and collection of information.

"""

from qutayba.Progress import (
    closeProgressBar,
    enableProgressBar,
    reportProgressBar,
    setupProgressBar,
)
from qutayba.Tracing import scons_logger


def enableSconsProgressBar():
    enableProgressBar()

    import atexit

    atexit.register(closeSconsProgressBar)


_total = None
_current = 0
_stage = None


def setSconsProgressBarTotal(name, total):
    # keep track of how many files there are to know when link comes, pylint: disable=global-statement
    global _total, _stage
    _total = total
    _stage = name

    setupProgressBar(stage="%s C" % name, unit="file", total=total)


def updateSconsProgressBar():
    # Check if link is next, pylint: disable=global-statement
    global _current
    _current += 1

    reportProgressBar(item=None, update=True)

    if _current == _total:
        closeSconsProgressBar()

        message = "%s C linking" % _stage

        if _total > 1:
            message += (
                " with %d files (no progress information available for this stage)"
                % _total
            )

        message += "."

        scons_logger.info(message)


def closeSconsProgressBar():
    closeProgressBar()


def reportSlowCompilation(env, cmd, delta_time):
    # TODO: for linking, we ought to apply a different timer maybe and attempt to extra
    # the source file that is causing the issues: pylint: disable=unused-argument
    if _current != _total:
        scons_logger.info(
            """\
Slow C compilation detected, used %.0fs so far, scalability problem."""
            % delta_time
        )
    else:
        if env.orig_lto_mode == "auto" and env.lto_mode:
            scons_logger.info(
                """\
Slow C linking detected, used %.0fs so far, consider using '--lto=no' \
for faster linking, or '--lto=yes"' to disable this message. """
                % delta_time
            )



