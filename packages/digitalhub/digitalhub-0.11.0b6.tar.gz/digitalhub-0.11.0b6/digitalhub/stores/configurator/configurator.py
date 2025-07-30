from __future__ import annotations

import os

from digitalhub.stores.configurator.credentials_store import CredentialsStore
from digitalhub.stores.configurator.enums import SetCreds
from digitalhub.stores.configurator.ini_module import load_from_file, read_env_from_file, set_current_env, write_config


class EnvConfigurator:
    """
    Configurator object used to configure clients and store credentials.
    """

    def __init__(self) -> None:
        # Store
        self._creds_store = CredentialsStore()

        # Current credentials set (__default by default)
        self._environment = os.getenv(SetCreds.DH_ENV.value, SetCreds.DEFAULT.value)

    ##############################
    # Public methods
    ##############################

    def set_current_env(self, creds_set: str) -> None:
        """
        Set the current credentials set.

        Parameters
        ----------
        creds_set : str
            Credentials set name.

        Returns
        -------
        None
        """
        self._environment = creds_set
        set_current_env(creds_set)

    def get_current_env(self) -> str:
        """
        Get the current credentials set.

        Returns
        -------
        str
            Credentials set name.
        """
        return self._environment

    ##############################
    # Private methods
    ##############################

    def load_var(self, var_name: str) -> str | None:
        """
        Get env variable from credentials store, env or file (in order).

        Parameters
        ----------
        var_name : str
            Environment variable name.

        Returns
        -------
        str | None
            Environment variable value.
        """
        var = self.get_credential(var_name)
        if var is None:
            var = self.load_from_env(var_name)
        if var is None:
            var = self.load_from_file(var_name)
        return var

    def load_from_env(self, var: str) -> str | None:
        """
        Load variable from env.

        Parameters
        ----------
        var : str
            Environment variable name.

        Returns
        -------
        str | None
            Environment variable value.
        """
        env_var = os.getenv(var)
        if env_var != "":
            return env_var

    def load_from_file(self, var: str) -> str | None:
        """
        Load variable from config file.

        Parameters
        ----------
        var : str
            Environment variable name.

        Returns
        -------
        str | None
            Environment variable value.
        """
        self._environment = read_env_from_file()
        return load_from_file(var)

    def write_env(self, key_to_include: list[str] | None = None) -> None:
        """
        Write the env variables to the .dhcore file.
        It will overwrite any existing env variables.

        Parameters
        ----------
        key_to_include : list[str]
            List of keys to include.

        Returns
        -------
        None
        """
        if key_to_include is None:
            key_to_include = []
        creds = self.get_credential_list(key_to_include)
        write_config(creds, self._environment)

    ##############################
    # Credentials store methods
    ##############################

    def set_credential(self, key: str, value: str) -> None:
        """
        Register a credential value.

        Parameters
        ----------
        key : str
            The key.
        value : str
            The value.

        Returns
        -------
        None
        """
        self._creds_store.set(self._environment, key, value)

    def get_credential(self, key: str) -> dict:
        """
        Get single credential value from key.

        Parameters
        ----------
        key : str
            The key.

        Returns
        -------
        dict
            The credential.
        """
        return self._creds_store.get(self._environment, key)

    def get_all_credentials(self) -> dict:
        """
        Get all the credentials from the current credentials set.

        Returns
        -------
        dict
            The credentials.
        """
        return self._creds_store.get_all(self._environment)

    def get_credential_list(self, keys: list[str]) -> list[str]:
        """
        Get the list of credentials.

        Parameters
        ----------
        keys : list[str]
            The list of keys.

        Returns
        -------
        list[str]
            The list of credentials.
        """
        return {k: v for k, v in self.get_all_credentials().items() if k in keys}


# Define global configurator
configurator = EnvConfigurator()
