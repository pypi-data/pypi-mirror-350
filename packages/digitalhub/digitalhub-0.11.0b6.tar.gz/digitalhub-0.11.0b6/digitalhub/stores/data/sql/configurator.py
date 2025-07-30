from __future__ import annotations

from digitalhub.stores.configurator.configurator import configurator
from digitalhub.stores.configurator.enums import CredsOrigin
from digitalhub.stores.data.sql.enums import SqlStoreEnv
from digitalhub.utils.exceptions import StoreError


class SqlStoreConfigurator:
    """
    Configure the store by getting the credentials from user
    provided config or from environment.
    """

    required_vars = [
        SqlStoreEnv.USERNAME,
        SqlStoreEnv.PASSWORD,
        SqlStoreEnv.HOST,
        SqlStoreEnv.PORT,
        SqlStoreEnv.DATABASE,
    ]

    ##############################
    # Configuration methods
    ##############################

    def get_sql_conn_string(self, origin: str) -> str:
        """
        Get the connection string from environment variables.

        Parameters
        ----------
        origin : str
            The origin of the credentials.

        Returns
        -------
        str
            The connection string.
        """
        if origin == CredsOrigin.ENV.value:
            creds = self._get_env_config()
        elif origin == CredsOrigin.FILE.value:
            creds = self._get_file_config()
        else:
            raise StoreError(f"Unknown origin: {origin}")

        user = creds[SqlStoreEnv.USERNAME.value]
        password = creds[SqlStoreEnv.PASSWORD.value]
        host = creds[SqlStoreEnv.HOST.value]
        port = creds[SqlStoreEnv.PORT.value]
        database = creds[SqlStoreEnv.DATABASE.value]
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

    def _get_env_config(self) -> dict:
        """
        Get the store configuration from environment variables.

        Returns
        -------
        dict
            The credentials.
        """
        credentials = {var.value: configurator.load_from_env(var.value) for var in self.required_vars}
        self._set_credentials(credentials)
        return credentials

    def _get_file_config(self) -> dict:
        """
        Get the store configuration from file.

        Returns
        -------
        dict
            The credentials.
        """
        credentials = {var.value: configurator.load_from_file(var.value) for var in self.required_vars}
        self._set_credentials(credentials)
        return credentials

    def _check_credentials(self, credentials: dict) -> None:
        """
        Check for missing credentials.

        Parameters
        ----------
        credentials : dict
            The credentials.

        Returns
        -------
        None
        """
        missing_vars = [key for key, value in credentials.items() if value is None and key in self.required_vars]
        if missing_vars:
            raise StoreError(f"Missing credentials for SQL store: {', '.join(missing_vars)}")

    def _set_credentials(self, credentials: dict) -> None:
        """
        Set the store credentials into the configurator.

        Parameters
        ----------
        credentials : dict
            The credentials.

        Returns
        -------
        None
        """
        # Set credentials
        for key, value in credentials.items():
            configurator.set_credential(key, value)
