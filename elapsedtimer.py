#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import print_function
import time
import sys

__all__ = ['ElapsedTimer']

# Global enable for printing timer results.
enable = True

# Select which clock routine is highest resolution for this OS.
if sys.platform == 'win32':
    hires_clock = time.clock
else:
    hires_clock = time.time

def get_time_units_and_multiplier(seconds):
    """
    Given a time in seconds, determines the best units and multiplier to
    use to display the time. Return value is a 2-tuple of units and multiplier.
    """
    table = [   (1e-9, u'ps', 1e12),
                (1e-6, u'ns', 1e9),
                (1e-3, u'µs', 1e6),
                (1.0,  u'ms', 1e3),
                (60,   u's',  1.0),
                (60*60, u'min', 1.0/60),
                (24*60*60, u'hrs', 1.0/(60*60)),
                (0, u's', 1.0)  ]   # Revert to seconds if very large
    for cutoff, units, multiplier in table:
        if seconds < cutoff:
            break
    return units, multiplier

def format_time(seconds):
    """Formats a number of seconds with the best units."""
    units, divider = get_time_units_and_multiplier(seconds)
    seconds *= divider
    return "%.3f %s" % (seconds, units)

class ElapsedTimer(object):
    """
    Timer meant to be used in a with statement. Pass the constructor an optional
    string describing the task that is being measured. When the with statement
    exits, a message will be printed to stdout with the elapsed time and the
    task description.
    """
    def __init__(self, task=''):
        self._task = task

    def __enter__(self):
        self._start = hires_clock()

    def __exit__(self, type, value, traceback):
        self._end = hires_clock()
        self._delta = self._end - self._start

        global enable
        if enable:
            displayDelta = format_time(self._delta)
            if len(self._task):
                print("%s: %s" % (displayDelta, self._task))
            else:
                print(displayDelta)

