import time
from datetime import datetime


def timestamp(prefix=None, postfix=None):
    stamp = time.strftime("%Y-%m-%d_%H:%M:%S")
    if prefix is not None:
        stamp = f"{prefix}_{stamp}"
    if postfix is not None:
        stamp = f"{stamp}_{postfix}"
    return stamp


def unix_time_ms():
    return int(time.time() * 1000)


def unix_time_us_ascii():
    unix_time_64bit = str(int(time.time() * 1000000))
    return unix_time_64bit.encode()


def cvt_unix_time_ms_to_datetime(unix_time_ms):
    sec = unix_time_ms / 1000
    us = (unix_time_ms % 1000) * 1000
    dt = datetime.fromtimestamp(sec)
    dt = dt.replace(microsecond=us)
    return dt
