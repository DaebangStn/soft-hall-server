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


def unix_time_byte():
    unix_time_64bit = str(int(time.time() * 1000000))
    return unix_time_64bit.encode()
