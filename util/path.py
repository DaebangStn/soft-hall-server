import os
from util.time import timestamp


def get_project_base():
    this_file = os.path.abspath(__file__)
    root_dir = os.path.dirname(os.path.dirname(this_file))
    return root_dir


def get_log_file_path(prefix=None, postfix=None):
    base = get_project_base()
    log_dir = os.path.join(base, "log")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_name = timestamp(prefix=prefix, postfix=postfix)
    log_path = os.path.join(log_dir, log_name)
    if os.path.exists(log_path):
        raise FileExistsError(f"Log file {log_path} already exists.")
    return log_path

