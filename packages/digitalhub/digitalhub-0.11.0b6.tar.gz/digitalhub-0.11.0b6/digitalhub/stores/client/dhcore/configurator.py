from __future__ import annotations

import typing
from warnings import warn

from requests import request

from digitalhub.stores.client.dhcore.enums import AuthType, DhcoreEnvVar
from digitalhub.stores.configurator.configurator import configurator
from digitalhub.stores.data.s3.enums import S3StoreEnv
from digitalhub.stores.data.sql.enums import SqlStoreEnv
from digitalhub.utils.exceptions import ClientError
from digitalhub.utils.generic_utils import list_enum
from digitalhub.utils.uri_utils import has_remote_scheme

if typing.TYPE_CHECKING:
    from requests import Response


# Default key used to store authentication information
AUTH_KEY = "_auth"

# API levels that are supported
MAX_API_LEVEL = 20
MIN_API_LEVEL = 11
LIB_VERSION = 11


class ClientDHCoreConfigurator:
    """
    Configurator object used to configure the client.
    """

    def __init__(self) -> None:
        self._current_env = configurator.get_current_env()

    ##############################
    # Configuration methods
    ##############################

    def check_config(self) -> None:
        """
        Check if the config is valid.

        Parameters
        ----------
        config : dict
            Configuration dictionary.

        Returns
        -------
        None
        """
        if configurator.get_current_env() != self._current_env:
            self.configure()

    def configure(self, config: dict | None = None) -> None:
        """
        Configure the client attributes with config (given or from
        environment).
        Regarding authentication parameters, the config parameter
        takes precedence over the env variables, and the token
        over the basic auth. Furthermore, the config parameter is
        validated against the proper pydantic model.

        Parameters
        ----------
        config : dict
            Configuration dictionary.

        Returns
        -------
        None
        """
        self._get_core_endpoint()
        self._get_auth_vars()

    def check_core_version(self, response: Response) -> None:
        """
        Raise an exception if DHCore API version is not supported.

        Parameters
        ----------
        response : Response
            The response object.

        Returns
        -------
        None
        """
        if "X-Api-Level" in response.headers:
            core_api_level = int(response.headers["X-Api-Level"])
            if not (MIN_API_LEVEL <= core_api_level <= MAX_API_LEVEL):
                raise ClientError("Backend API level not supported.")
            if LIB_VERSION < core_api_level:
                warn("Backend API level is higher than library version. You should consider updating the library.")

    def build_url(self, api: str) -> str:
        """
        Build the url.

        Parameters
        ----------
        api : str
            The api to call.

        Returns
        -------
        str
            The url.
        """
        api = api.removeprefix("/")
        return f"{configurator.get_credential(DhcoreEnvVar.ENDPOINT.value)}/{api}"

    ##############################
    # Private methods
    ##############################

    @staticmethod
    def _sanitize_endpoint(endpoint: str) -> str:
        """
        Sanitize the endpoint.

        Returns
        -------
        None
        """
        if not has_remote_scheme(endpoint):
            raise ClientError("Invalid endpoint scheme. Must start with http:// or https://.")

        endpoint = endpoint.strip()
        return endpoint.removesuffix("/")

    def _get_core_endpoint(self) -> None:
        """
        Get the DHCore endpoint from env.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the endpoint of DHCore is not set in the env variables.
        """
        endpoint = configurator.load_var(DhcoreEnvVar.ENDPOINT.value)
        if endpoint is None:
            raise ClientError("Endpoint not set as environment variables.")
        endpoint = self._sanitize_endpoint(endpoint)
        configurator.set_credential(DhcoreEnvVar.ENDPOINT.value, endpoint)

    def _get_auth_vars(self) -> None:
        """
        Get authentication parameters from the env.

        Returns
        -------
        None
        """
        # Give priority to access token
        access_token = self._load_dhcore_oauth_vars(DhcoreEnvVar.ACCESS_TOKEN.value)
        if access_token is not None:
            configurator.set_credential(AUTH_KEY, AuthType.OAUTH2.value)
            configurator.set_credential(DhcoreEnvVar.ACCESS_TOKEN.value.removeprefix("DHCORE_"), access_token)

        # Fallback to basic
        else:
            user = configurator.load_var(DhcoreEnvVar.USER.value)
            password = configurator.load_var(DhcoreEnvVar.PASSWORD.value)
            if user is not None and password is not None:
                configurator.set_credential(AUTH_KEY, AuthType.BASIC.value)
                configurator.set_credential(DhcoreEnvVar.USER.value, user)
                configurator.set_credential(DhcoreEnvVar.PASSWORD.value, password)

    ##############################
    # Auth methods
    ##############################

    def basic_auth(self) -> bool:
        """
        Get basic auth.

        Returns
        -------
        bool
        """
        auth_type = configurator.get_credential(AUTH_KEY)
        return auth_type == AuthType.BASIC.value

    def oauth2_auth(self) -> bool:
        """
        Get oauth2 auth.

        Returns
        -------
        bool
        """
        auth_type = configurator.get_credential(AUTH_KEY)
        return auth_type == AuthType.OAUTH2.value

    def set_request_auth(self, kwargs: dict) -> dict:
        """
        Get the authentication header.

        Parameters
        ----------
        kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Authentication header.
        """
        creds = configurator.get_all_credentials()
        if AUTH_KEY not in creds:
            return kwargs
        if self.basic_auth():
            user = creds[DhcoreEnvVar.USER.value]
            password = creds[DhcoreEnvVar.PASSWORD.value]
            kwargs["auth"] = (user, password)
        elif self.oauth2_auth():
            if "headers" not in kwargs:
                kwargs["headers"] = {}
            access_token = creds[DhcoreEnvVar.ACCESS_TOKEN.value.removeprefix("DHCORE_")]
            kwargs["headers"]["Authorization"] = f"Bearer {access_token}"
        return kwargs

    def get_new_access_token(self) -> None:
        """
        Get a new access token.

        Returns
        -------
        None
        """
        # Call issuer and get endpoint for
        # refreshing access token
        url = self._get_refresh_endpoint()

        # Call refresh token endpoint
        # Try token from env
        refresh_token = configurator.load_from_env(DhcoreEnvVar.REFRESH_TOKEN.value)
        response = self._call_refresh_token_endpoint(url, refresh_token)

        # Otherwise try token from file
        if response.status_code in (400, 401, 403):
            refresh_token = configurator.load_from_file(DhcoreEnvVar.REFRESH_TOKEN.value.removeprefix("DHCORE_"))
            response = self._call_refresh_token_endpoint(url, refresh_token)

        response.raise_for_status()

        # Read new credentials and propagate to config file
        self._set_creds(response.json())

    def _set_creds(self, response: dict) -> None:
        """
        Set new credentials.

        Parameters
        ----------
        response : dict
            Response from refresh token endpoint.

        Returns
        -------
        None
        """
        keys = [
            *self._remove_prefix_dhcore(list_enum(DhcoreEnvVar)),
            *list_enum(S3StoreEnv),
            *list_enum(SqlStoreEnv),
        ]
        for key in keys:
            if (value := response.get(key.lower())) is not None:
                configurator.set_credential(key, value)
        configurator.write_env(keys)

    def _remove_prefix_dhcore(self, keys: list[str]) -> list[str]:
        """
        Remove prefix from selected keys. (Compatibility with CLI)

        Parameters
        ----------
        keys : list[str]
            List of keys.

        Returns
        -------
        list[str]
            List of keys without prefix.
        """
        new_list = []
        for key in keys:
            if key in (
                DhcoreEnvVar.REFRESH_TOKEN.value,
                DhcoreEnvVar.ACCESS_TOKEN.value,
                DhcoreEnvVar.ISSUER.value,
                DhcoreEnvVar.CLIENT_ID.value,
            ):
                new_list.append(key.removeprefix("DHCORE_"))
            else:
                new_list.append(key)
        return new_list

    def _get_refresh_endpoint(self) -> str:
        """
        Get the refresh endpoint.

        Returns
        -------
        str
            Refresh endpoint.
        """
        # Get issuer endpoint
        endpoint_issuer = self._load_dhcore_oauth_vars(DhcoreEnvVar.ISSUER.value)
        if endpoint_issuer is None:
            raise ClientError("Issuer endpoint not set.")
        endpoint_issuer = self._sanitize_endpoint(endpoint_issuer)
        configurator.set_credential(DhcoreEnvVar.ISSUER.value.removeprefix("DHCORE_"), endpoint_issuer)

        # Standard issuer endpoint path
        url = endpoint_issuer + "/.well-known/openid-configuration"

        # Call issuer to get refresh endpoint
        r = request("GET", url, timeout=60)
        r.raise_for_status()
        return r.json().get("token_endpoint")

    def _call_refresh_token_endpoint(self, url: str, refresh_token: str) -> Response:
        """
        Call the refresh token endpoint.

        Parameters
        ----------
        url : str
            Refresh token endpoint.
        refresh_token : str
            Refresh token.

        Returns
        -------
        Response
            Response object.
        """
        # Get client id
        client_id = self._load_dhcore_oauth_vars(DhcoreEnvVar.CLIENT_ID.value)
        if client_id is None:
            raise ClientError("Client id not set.")

        # Send request to get new access token
        payload = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": refresh_token,
            "scope": "openid credentials offline_access",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return request("POST", url, data=payload, headers=headers, timeout=60)

    def _load_dhcore_oauth_vars(self, oauth_var: str) -> str | None:
        """
        Load DHCore oauth variables.

        Parameters
        ----------
        oauth_var : str
            The oauth variable to load.

        Returns
        -------
        str
            The oauth variable.
        """
        read_var = configurator.load_from_env(oauth_var)
        if read_var is None:
            read_var = configurator.load_from_file(oauth_var.removeprefix("DHCORE_"))
        return read_var
