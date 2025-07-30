from __future__ import annotations

from botocore.config import Config

from digitalhub.stores.configurator.configurator import configurator
from digitalhub.stores.configurator.enums import CredsOrigin
from digitalhub.stores.data.s3.enums import S3StoreEnv
from digitalhub.utils.exceptions import StoreError


class S3StoreConfigurator:
    """
    Configure the store by getting the credentials from user
    provided config or from environment.
    """

    required_vars = [
        S3StoreEnv.ENDPOINT_URL,
        S3StoreEnv.ACCESS_KEY_ID,
        S3StoreEnv.SECRET_ACCESS_KEY,
    ]
    optional_vars = [
        S3StoreEnv.REGION,
        S3StoreEnv.SIGNATURE_VERSION,
        S3StoreEnv.SESSION_TOKEN,
    ]

    ##############################
    # Configuration methods
    ##############################

    def get_boto3_client_config(self, origin: str) -> dict:
        """
        Get S3 credentials (access key, secret key,
        session token and other config).

        Parameters
        ----------
        origin : str
            The origin of the credentials.

        Returns
        -------
        dict
            The credentials.
        """
        if origin == CredsOrigin.ENV.value:
            creds = self._get_env_config()
        elif origin == CredsOrigin.FILE.value:
            creds = self._get_file_config()
        else:
            raise StoreError(f"Unknown origin: {origin}")
        return {
            "endpoint_url": creds[S3StoreEnv.ENDPOINT_URL.value],
            "aws_access_key_id": creds[S3StoreEnv.ACCESS_KEY_ID.value],
            "aws_secret_access_key": creds[S3StoreEnv.SECRET_ACCESS_KEY.value],
            "aws_session_token": creds[S3StoreEnv.SESSION_TOKEN.value],
            "config": Config(
                region_name=creds[S3StoreEnv.REGION.value],
                signature_version=creds[S3StoreEnv.SIGNATURE_VERSION.value],
            ),
        }

    def _get_env_config(self) -> dict:
        """
        Get the store configuration from environment variables.

        Returns
        -------
        dict
            The credentials.
        """
        credentials = {
            var.value: configurator.load_from_env(var.value) for var in self.required_vars + self.optional_vars
        }
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
        credentials = {
            var.value: configurator.load_from_file(var.value) for var in self.required_vars + self.optional_vars
        }
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
            raise StoreError(f"Missing credentials for S3 store: {', '.join(missing_vars)}")

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
