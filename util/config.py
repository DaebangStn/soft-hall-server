import os
import yaml
from util.path import get_project_base


def default_yaml_path():
    return os.path.join(get_project_base(), "config.yaml")


def load_config(path: str = None):
    if path is None:
        path = default_yaml_path()
    with open(path, 'r') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf
