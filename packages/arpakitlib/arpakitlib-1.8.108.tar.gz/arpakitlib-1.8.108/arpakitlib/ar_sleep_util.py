# arpakit

import asyncio
import math
from time import sleep

from asyncpg.pgproto.pgproto import timedelta

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def sync_safe_sleep(n: timedelta | float | int):
    if isinstance(n, timedelta):
        n = n.total_seconds()
    elif isinstance(n, int):
        n = float(n)
    elif isinstance(n, float):
        n = n
    else:
        raise TypeError(f"n={n}, type={type(n)}, n: timedelta | float | int")

    n: float = n

    frac, int_part = math.modf(n)
    for i in range(int(int_part)):
        sleep(1)
    sleep(frac)


async def async_safe_sleep(n: timedelta | float | int):
    if isinstance(n, timedelta):
        n = n.total_seconds()
    elif isinstance(n, int):
        n = float(n)
    elif isinstance(n, float):
        n = n
    else:
        raise TypeError(f"n={n}, type={type(n)}, n: timedelta | float | int")

    n: float = n

    await asyncio.sleep(n)


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
