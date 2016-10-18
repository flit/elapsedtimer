#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright (c) 2014-2016 Chris Reed
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# o Redistributions of source code must retain the above copyright notice, this list
#   of conditions and the following disclaimer.
#
# o Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
# o Neither the name of Chris Reed nor the names of contributors may be used to
#   endorse or promote products derived from this software without specific prior
#   written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import print_function
import datetime
import sys
import logging
try:
    from time import monotonic as hires_clock
except ImportError:
    import time
    # Select which clock routine is highest resolution for this OS.
    if sys.platform == 'win32':
        hires_clock = time.clock
    else:
        hires_clock = time.time

__all__ = ['ElapsedTimer', 'Timeout', 'TimeoutError']

__version__ = '0.4'

# Global enable for printing timer results.
enable = True

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

class TimeoutError(RuntimeError):
    pass

class ElapsedTimer(object):
    """
    Timer meant to be used in a with statement. Pass the constructor an optional
    string describing the task that is being measured. When the with statement
    exits, a message will be printed to stdout with the elapsed time and the
    task description.
    """
    def __init__(self, task='', output=sys.stdout, logger=None, loglevel=logging.DEBUG):
        self._task = task
        self._start = 0
        self._end = 0
        self._delta = 0
        self._enable = True
        self._file = output
        self._logger = logger
        self._loglevel = loglevel

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        self._print_message()

    def start(self):
        self._start = hires_clock()
        self._end = 0
        self._delta = 0

    def stop(self):
        if self._end == 0:
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
                msg = "%s: %s" % (displayDelta, self._task)
            else:
                msg = displayDelta
            if not self._logger:
                msg += '\n'
            if self._logger:

                self._logger.log(self._loglevel, msg)
            else:
                self._file.write(msg)

class Timeout(ElapsedTimer):
    def __init__(self, timeout=0, task='', output=sys.stdout, logger=None, loglevel=logging.DEBUG):
        super(Timeout, self).__init__(task, output, logger, loglevel)
        self._timeout = timeout
        self._did_timeout = False

    def check(self):
        if self._timeout is None:
            return False
        if self._did_timeout:
            return True
        self._did_timeout = self.elapsed >= self._timeout
        return self._did_timeout

    def check_and_raise(self):
        if self.check():
            raise TimeoutError(self._task)

    @property
    def timed_out(self):
        return self.check()
