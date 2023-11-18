import time


def timestamp(prefix=None, postfix=None):
    stamp = time.strftime("%Y-%m-%d_%H:%M:%S")
    if prefix is not None:
        stamp = f"{prefix}_{stamp}"
    if postfix is not None:
        stamp = f"{stamp}_{postfix}"
    return stamp


def unix_time():
    return int(time.time())
