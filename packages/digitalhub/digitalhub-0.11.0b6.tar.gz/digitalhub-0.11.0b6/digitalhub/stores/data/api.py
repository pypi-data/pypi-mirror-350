from __future__ import annotations

import typing

from digitalhub.stores.data.builder import store_builder

if typing.TYPE_CHECKING:
    from digitalhub.stores.data._base.store import Store


def get_store(project: str, uri: str) -> Store:
    """
    Get store instance by URI.

    Parameters
    ---------
    project : str
        Project name.
    uri : str
        URI to parse.
    config : dict
        Store configuration.

    Returns
    -------
    Store
        Store instance.
    """
    return store_builder.get(project, uri)
