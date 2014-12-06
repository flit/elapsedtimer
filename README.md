elapsedtimer
============

Python elapsed time utilities.

The main interface to this package is an ``ElapsedTimer`` class. This class will use the highest
resolution timer available to Python depending on the OS, either ``time.time()`` or
``time.clock()``. Its purpose is easily to measure and print the duration of a task, and is
normally meant to be used as a context manager.

Basic example:

    >>> with ElapsedTimer('say hello'):
    ...     print 'hi there!'
    hi there!
    13.113 µs: say hello

The constructor for ``ElapsedTimer`` takes an optional string describing the operation being
performed. It also optionally accepts a file object to change where the resulting duration
message will be printed. The output file defaults to sys.stdout.

You can control an ``ElapsedTimer`` instance directly instead of using it as a context manager.
It has ``start()`` and ``stop()`` methods. The ``stop()`` method will not print the duration for
you like exiting a context manager instance does.

There is an ``elapsed`` property that returns the elapsed time since ``start()`` was called or the
context manager entered. A ``timedelta`` property is also available that returns the elapsed
time as a datetime.timedelta object instead of a float, though note that this class this only has
microsecond resolution.

In addition to ``ElapsedTimer``, there are some utilities. The ``format_duration()`` function
takes a duration in seconds and returns a string with the most human-readable duration and time
units. The units are selected such that there will be between 1 and 3 digits before the decimal
point.

There is a module-level ``enable`` variable that acts as a global enable switch for all printing
of results by ``ElapsedTimer``. It defaults to True.

License
-------

This package is licensed under the BSD three-clause license. See the LICENSE file for details.

Copyright © 2014 Chris Reed.

