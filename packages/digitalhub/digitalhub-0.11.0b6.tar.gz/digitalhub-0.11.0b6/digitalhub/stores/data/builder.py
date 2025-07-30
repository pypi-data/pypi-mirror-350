from __future__ import annotations

import typing

from digitalhub.stores.configurator.api import get_current_env
from digitalhub.stores.data.local.store import LocalStore
from digitalhub.stores.data.remote.store import RemoteStore
from digitalhub.stores.data.s3.store import S3Store
from digitalhub.stores.data.sql.store import SqlStore
from digitalhub.utils.uri_utils import SchemeCategory, map_uri_scheme

if typing.TYPE_CHECKING:
    from digitalhub.stores.data._base.store import Store


def _get_class_from_type(type: str) -> Store:
    """
    Get a store class from its type.

    Parameters
    ----------
    type : str
        Store type.

    Returns
    -------
    Store
        The store class.
    """
    if type == SchemeCategory.LOCAL.value:
        return LocalStore
    if type == SchemeCategory.S3.value:
        return S3Store
    if type == SchemeCategory.REMOTE.value:
        return RemoteStore
    if type == SchemeCategory.SQL.value:
        return SqlStore
    raise ValueError(f"Unknown store type: {type}")


class StoreBuilder:
    """
    Store builder class.
    """

    def __init__(self) -> None:
        self._instances: dict[str, dict[str, Store]] = {}

    def build(self, project: str, store_type: str) -> None:
        """
        Build a store instance and register it.

        Parameters
        ----------
        store_type : str
            Store type.
        config : dict

        Returns
        -------
        None
        """
        env = get_current_env()
        if env not in self._instances:
            self._instances[env] = {}
        self._instances[env][store_type] = _get_class_from_type(store_type)()

    def get(self, project: str, uri: str) -> Store:
        """
        Get a store instance by URI.

        Parameters
        ----------
        uri : str
            URI to parse.
        config : dict
            Store configuration.

        Returns
        -------
        Store
            The store instance.
        """
        env = get_current_env()
        store_type = map_uri_scheme(uri)
        try:
            return self._instances[env][store_type]
        except KeyError:
            self.build(project, store_type)
            return self._instances[env][store_type]


store_builder = StoreBuilder()
