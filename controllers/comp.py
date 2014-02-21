# -*- coding: utf-8 -*-
""" ``comp`` module.
"""

import sys


PY_MAJOR = sys.version_info[0]
PY_MINOR = sys.version_info[1]
PY2 = PY_MAJOR == 2
PY3 = PY_MAJOR >= 3


if PY3:  # pragma: nocover
    iteritems = lambda d: d.items()
    itervalues = lambda d: d.values()
    xrange = range
    string_type = str
else:  # pragma: nocover
    iteritems = lambda d: d.iteritems()
    itervalues = lambda d: d.itervalues()
    xrange = xrange
    string_type = unicode


if PY3:  # pragma: nocover
    from _thread import allocate_lock
else:  # pragma: nocover
    from thread import allocate_lock  # noqa

if PY2 and PY_MINOR == 4:  # pragma: nocover
    __import__ = __import__
else:  # pragma: nocover
    # perform absolute import
    __saved_import__ = __import__
    __import__ = lambda n, g=None, l=None, f=None: \
        __saved_import__(n, g, l, f, 0)

if PY3:  # pragma: nocover
    from queue import Queue
else:  # pragma: nocover
    from Queue import Queue  # noqa
