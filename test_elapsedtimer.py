#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright (c) 2015 Chris Reed
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

import elapsedtimer
from elapsedtimer import *
import pytest
import time
import datetime

def within(x, y, r):
    print "within(%f, %f, %f)" % (x, y, r)
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
    print "count_for_time(%g) = %g" % (e,x)
    return int(x)

class TestElapsedTimer:
    def test_start_stop(self):
        startTime = time.time()
        t = ElapsedTimer('foo')
        t.start()
        for i in range(count_for_time(0.02)): pass
        t.stop()

        assert within(t.elapsed, time.time() - startTime, 0.01)

    def test_timedelta(self):
        startTime = time.time()
        t = ElapsedTimer('foo')
        t.start()
        for i in range(count_for_time(0.02)): pass
        t.stop()
        d = datetime.timedelta(seconds=(time.time() - startTime))

        assert (t.timedelta - d) < datetime.timedelta(seconds=0.01)

    def test_context(self):
        startTime = time.time()
        with ElapsedTimer('foo') as t:
            for i in range(1000): pass
        assert within(t.elapsed, time.time() - startTime, 0.01)

class TestTimeout:
    def test_check(self):
        with Timeout(0.4, 'foo') as t:
            for i in range(count_for_time(0.5)):
                if t.check():
                    break
            assert t.timed_out

    def test_check_and_raise(self):
        with pytest.raises(TimeoutError):
            cnt = count_for_time(0.5)
            with Timeout(0.4, 'foo') as t:
                for i in range(cnt):
                    if t.check_and_raise():
                        break

