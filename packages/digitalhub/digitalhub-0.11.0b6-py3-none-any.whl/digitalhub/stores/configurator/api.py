from __future__ import annotations

from digitalhub.stores.configurator.configurator import configurator


def set_current_env(environment: str) -> None:
    """
    Set the current credentials set.

    Parameters
    ----------
    environment : str
        Credentials set name.

    Returns
    -------
    None
    """
    configurator.set_current_env(environment)


def get_current_env() -> str:
    """
    Get the current credentials set.

    Returns
    -------
    str
        Credentials set name.
    """
    return configurator.get_current_env()
