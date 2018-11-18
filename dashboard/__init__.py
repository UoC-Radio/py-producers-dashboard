from itertools import chain
from time import time
import logging

logger = logging.getLogger(__name__)
tabbing = 0


def log(fn):
    """Decorator to log function details.

    Shows function signature, return value, time elapsed, etc.
    Logging will be done if the debug flag is set.
    :param fn: the function to be decorated
    :return: function wrapped for logging
    """
    if logger.getEffectiveLevel() > logging.DEBUG:
        return fn

    def wrapped(*v, **k):
        global tabbing
        name = fn.__qualname__
        filename = fn.__code__.co_filename.split('/')[-1]
        lineno = fn.__code__.co_firstlineno

        params = ", ".join(map(repr, chain(v, k.values())))

        if 'rateLimitedFunction' not in name:
            logger.debug("%s%s(%s)[%s:%s]", '|' * tabbing, name, params,
                         filename, lineno)
        tabbing += 1
        start = time()
        retval = fn(*v, **k)
        elapsed = time() - start
        tabbing -= 1
        elapsed_time = ''
        if elapsed > 0.1:
            elapsed_time = ', took %02f' % elapsed
        if (elapsed_time
                or retval is not None):
            if 'rateLimitedFunction' not in name:
                logger.debug("%s  returned %s%s", '|' * tabbing, repr(retval),
                             elapsed_time)
        return retval

    return wrapped

