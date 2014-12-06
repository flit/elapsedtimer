#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import print_function
import time
import datetime
import sys
import logging

__all__ = ['ElapsedTimer']

# Global enable for printing timer results.
enable = True

# Select which clock routine is highest resolution for this OS.
if sys.platform == 'win32':
    hires_clock = time.clock
else:
    hires_clock = time.time

## Table of time units.
#
# List elements are a 3-tuple containing:
# - Cutoff value for this entry. The entry should be used if the time value is less
#   than this cutoff.
# - Unit string.
# - Multiplier to convert the time value to this entry's units.
units_table = [   (1e-9, u'ps', 1e12),
            (1e-6, u'ns', 1e9),
            (1e-3, u'µs', 1e6),
            (1.0,  u'ms', 1e3),
            (60,   u's',  1.0),
            (60*60, u'min', 1.0/60),
            (24*60*60, u'hrs', 1.0/(60*60)),
            (0, u's', 1.0)  ]   # Revert to seconds if very large

def get_time_units_and_multiplier(seconds):
    """
    Given a duration in seconds, determines the best units and multiplier to
    use to display the time. Return value is a 2-tuple of units and multiplier.
    """
    for cutoff, units, multiplier in units_table:
        if seconds < cutoff:
            break
    return units, multiplier

def format_duration(seconds):
    """Formats a number of seconds using the best units."""
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
    def __init__(self, task='', output=sys.stdout):
        self._task = task
        self._start = 0
        self._end = 0
        self._delta = 0
        self._enable = True
        self._file = output

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        self.stop()
        self._print_message()

    def start(self):
        self._start = hires_clock()

    def stop(self):
        self._end = hires_clock()
        self._delta = self._end - self._start

    @property
    def enable(self):
        return self._enable

    @enable.setter
    def enable(self, value):
        self._enable = value

    @property
    def elapsed(self):
        if self._end:
            return self._delta
        else:
            return hires_clock() - self._start

    @property
    def timedelta(self):
        return datetime.timedelta(seconds=self.elapsed)

    def _print_message(self):
        global enable
        if enable and self._enable:
            displayDelta = format_duration(self._delta)
            if len(self._task):
                msg = "%s: %s\n" % (displayDelta, self._task)
            else:
                msg = displayDelta + '\n'
            self._file.write(msg)

