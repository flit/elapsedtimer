#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright (c) 2015-2022 Chris Reed
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

import pytest
import time
import datetime
from sys import platform, version_info

import elapsedtimer
from elapsedtimer import (
    ElapsedTimer,
    Timeout,
)

def within(x, y, r):
    print("within(%f, %f, %f)" % (x, y, r))
    return abs(x - y) < r

def calibrate():
    startTime = time.time()
    for i in range(1000): pass
    stopTime = time.time()
    timePer1000 = stopTime - startTime
    return timePer1000

timePer1000 = calibrate()

def count_for_time(e):
    x = 1000 * e / timePer1000
    print("count_for_time(%g) = %g" % (e,x))
    return int(x)

@pytest.mark.skipif(version_info < (3,3), reason='Requires python >= 3.3')
def test_module_uses_monotonic_as_timer():
    '''Assert that time.monotonic is used.'''
    assert elapsedtimer.hires_clock == time.monotonic

@pytest.mark.skipif(version_info > (3,2), reason='Using python >= 3.3')
@pytest.mark.skipif(platform == 'win32', reason='Requires other platform than windows.')
def test_module_uses_time_as_timer():
    '''Assert that time.time is used (on non windows platforms) when time.monotonic is not available.'''
    assert elapsedtimer.hires_clock == time.time

@pytest.mark.skipif(version_info > (3,2), reason='Using python >= 3.3')
@pytest.mark.skipif(platform != 'win32', reason='Requires windows platform.')
def test_module_uses_clock_as_timer():
    '''Assert that time.time is used when time.monotonic is not available.'''
    assert elapsedtimer.hires_clock == time.clock

def delay_for_a_bit():
    for i in range(100):
        time.sleep(0.001)

class TestElapsedTimer:
    def test_start_stop(self):
        start_time = time.time()
        t = ElapsedTimer('foo')
        t.start()
        delay_for_a_bit()
        t.stop()
        stop_time = time.time()

        assert within(t.elapsed, stop_time - start_time, 0.01)

    def test_timedelta(self):
        start_time = time.time()
        t = ElapsedTimer('foo')
        t.start()
        delay_for_a_bit()
        t.stop()
        stop_time = time.time()
        d = datetime.timedelta(seconds=(stop_time - start_time))

        assert (t.timedelta - d) < datetime.timedelta(seconds=0.01)

    def test_context(self):
        start_time = time.time()
        with ElapsedTimer('foo') as t:
            delay_for_a_bit()
        stop_time = time.time()
        assert within(t.elapsed, stop_time - start_time, 0.01)

# class TestTimeout:
#     def test_check(self):
#         with Timeout(0.4, 'foo') as t:
#             for i in range(count_for_time(0.5)):
#                 if t.check():
#                     break
#             assert t.timed_out
#
#     def test_check_and_raise(self):
#         with pytest.raises(TimeoutError):
#             cnt = count_for_time(0.5)
#             with Timeout(0.4, 'foo') as t:
#                 for i in range(cnt):
#                     if t.check_and_raise():
#                         break

