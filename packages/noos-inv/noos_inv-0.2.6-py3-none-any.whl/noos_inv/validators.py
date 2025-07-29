import pathlib
from collections.abc import Mapping

from noos_inv import exceptions, types


def check_path(path: str) -> None:
    """Check whether a path exists on a file system."""
    if not pathlib.Path(path).exists():
        raise exceptions.PathNotFound(f"Incorrect file system path: {path}")


def check_config(config: object) -> None:
    """Check whether a port-forward configuration is valid."""
    if not isinstance(config, Mapping):
        raise exceptions.InvalidConfig("Configuration must be an mapping")
    if len(config) == 0:
        raise exceptions.InvalidConfig("Configuration can not be empty")
    for item in config.values():
        if not isinstance(item, Mapping):
            raise exceptions.InvalidConfig("Configuration element must be a mapping")
        if not (types.PodConfig.__required_keys__ <= set(item.keys())):
            raise exceptions.InvalidConfig("Invalid configuration element keys")
