import resource
import sys
import time
from functools import partial

print2 = partial(print, file=sys.stderr)


def peakmem() -> int:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


__lasttime: float = 0


def stopwatch() -> float:
    global __lasttime  # noqa: PLW0603

    now: float = time.perf_counter()
    diff: float = now - __lasttime
    __lasttime = now

    return diff
