from __future__ import annotations

from digitalhub.context.api import get_context
from digitalhub.stores.configurator.configurator import configurator
from digitalhub.stores.data.enums import StoreEnv


def get_default_store(project: str) -> str:
    """
    Get default store URI.

    Parameters
    ----------
    project : str
        Project name.

    Returns
    -------
    str
        Default store URI.
    """
    context = get_context(project)
    store = context.config.get(StoreEnv.DEFAULT_FILES_STORE.value.lower())
    if store is not None:
        return store
    store = configurator.load_var(StoreEnv.DEFAULT_FILES_STORE.value)
    if store is None or store == "":
        raise ValueError(
            "No default store found. "
            "Please set a default store "
            f"in your environment (e.g. export {StoreEnv.DEFAULT_FILES_STORE.value}=) "
            "or set it in project config."
        )
    return store
