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

ElapsedTimer
------------

The constructor for ``ElapsedTimer`` takes an optional string describing the operation being
performed. It also optionally accepts a file object to change where the resulting duration
message will be printed. The output file defaults to sys.stdout.

The constructor can also take a logger instance and log level via the optional ``logger`` and
``loglevel`` keyword parameters. If a logger is provided, it takes precedence over a file object
and the duration message will be output via the logger. The log level defaults to ``DEBUG``.

You can control an ``ElapsedTimer`` instance directly instead of using it as a context manager.
It has ``start()`` and ``stop()`` methods. The ``stop()`` method will not print the duration for
you like exiting a context manager instance does.

There is an ``elapsed`` property that returns the elapsed time since ``start()`` was called or the
context manager entered. A ``timedelta`` property is also available that returns the elapsed
time as a datetime.timedelta object instead of a float, though note that this class this only has
microsecond resolution.

There is a module-level ``enable`` variable that acts as a global enable switch for all printing
of results by ``ElapsedTimer``. It defaults to True.

Timeout
-------

Another class in the module is ``Timeout``. It adds a few methods to make it easy to check for
timeouts. You can use this class as a context manager. The constructor takes the same parameters
as for ``ElapsedTimer``, except for a new first param of the timeout in seconds.

There are two methods to check the timeout, ``check()`` and ``check_and_raise()``. The former
compares the elapsed time against the timeout and returned True if a timeout occurred. The latter
will raise ``TimeoutError`` if a timeout happens. You can use the ``timed_out`` property to
as another way to check, equivalent to calling ``check()``.


License
-------

This package is licensed under the BSD three-clause license. See the LICENSE file for details.

Copyright © 2014-2016 Chris Reed.

