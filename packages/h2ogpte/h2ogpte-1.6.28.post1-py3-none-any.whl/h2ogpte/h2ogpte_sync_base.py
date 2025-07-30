import json
import asyncio
import nest_asyncio
import requests
import uuid
from typing import Any, Union, Dict, Optional, Callable
from h2o_authn import TokenProvider

from h2ogpte.errors import (
    ErrorResponse,
    HTTPError,
    InternalServerError,
    InvalidArgumentError,
    ObjectNotFoundError,
    UnauthorizedError,
)
from h2ogpte.h2ogpte_async import H2OGPTEAsync
from h2ogpte.types import SessionError, Identifier
from h2ogpte.session import Session


class H2OGPTESyncBase:
    # Timeout for HTTP requests
    TIMEOUT = 3600.0

    def __init__(
        self,
        address: str,
        api_key: Optional[str] = None,
        token_provider: Optional[TokenProvider] = None,
        verify: Union[bool, str] = True,
        strict_version_check: bool = False,
    ):
        """Create a new H2OGPTE client.

        Args:
            address:
                Full URL of the h2oGPTe server to connect to, e.g. "https://h2ogpte.h2o.ai".
            api_key:
                API key for authentication to the h2oGPTe server. Users can generate
                a key by accessing the UI and navigating to the Settings.
            token_provider:
                User's token provider.
            verify:
                Whether to verify the server's TLS/SSL certificate.
                Can be a boolean or a path to a CA bundle.
                Defaults to True.
            strict_version_check:
                Indicate whether a version check should be enforced.

        Returns:
            A new H2OGPTE client.
        """
        # Remove trailing slash from address, if any
        address = address.rstrip("/ ")

        self._address = address
        self._api_key = api_key
        self._verify = verify
        self._token_provider = token_provider
        self._session_id = str(uuid.uuid4())

        if self._api_key is None and self._token_provider is None:
            raise RuntimeError(
                f"Please use either an API key or a Token provider to authenticate."
            )

        if self._api_key is not None and self._token_provider is not None:
            print(
                "Warning: The token_provider parameter will be ignored in favor of the provided api_key"
            )

        self._check_version(strict_version_check)

    def _async_client(self):
        token_provider = None
        if self._token_provider is not None:
            token_provider = self._token_provider.as_async()
        return H2OGPTEAsync(
            self._address, self._api_key, token_provider, self._verify, False
        )

    def _run_async(self, async_method_wrapper: Callable[[H2OGPTEAsync], Any]):
        loop = asyncio._get_running_loop()
        if loop is not None:
            nest_asyncio.apply(loop)

        async def call():
            async with self._async_client() as c:
                return await async_method_wrapper(c)

        return asyncio.run(call())

    def _get_auth_header(self) -> Dict:
        if self._api_key is not None:
            return {
                "Authorization": f"Bearer {self._api_key}",
            }
        elif self._token_provider is not None:
            token = self._token_provider.token()
            return {
                "Authorization": f"Token-Bearer {token}",
                "Session-Id": self._session_id,
            }
        else:
            raise Exception(
                "Please provide either an api_key or a token_provider to authenticate."
            )

    def _check_version(self, strict_version_check: bool):
        from h2ogpte import __version__ as client_version

        server_version = self.get_meta().version
        if client_version.count(".") == 3:
            client_version = client_version[: client_version.rfind(".")]
        if server_version.count(".") == 3:
            server_version = server_version[: server_version.rfind(".")]

        if server_version[0] == "v":
            server_version = server_version[1:]

        if server_version != client_version:
            msg = (
                f"Warning: Server version {server_version} doesn't match client "
                f"version {client_version}: unexpected errors may occur.\n"
                f"Please install the correct version of H2OGPTE "
                f"with `pip install h2ogpte=={server_version}`."
            )
            if strict_version_check:
                raise RuntimeError(msg)
            else:
                print(msg)
                print(
                    "You can enable strict version checking by passing strict_version_check=True."
                )

    def _post(self, slug: str, data: Any):
        res = requests.post(
            f"{self._address}{slug}",
            data=data,
            headers={**self._get_auth_header(), **{"Content-Type": "application/json"}},
            verify=self._verify,
            timeout=H2OGPTESyncBase.TIMEOUT,
        )
        self._raise_error_if_any(res)
        return res.json()

    def _post_stream(self, slug: str, data: Any, custom_headers: dict = None):
        headers = {
            **self._get_auth_header(),
            "Content-Type": "application/json",
            **(custom_headers or {}),
        }
        res = requests.post(
            f"{self._address}{slug}",
            data=data,
            headers=headers,
            verify=self._verify,
            timeout=H2OGPTESyncBase.TIMEOUT,
            stream=True,
        )
        res.raise_for_status()
        return res

    def _raise_error_if_any(self, res: requests.Response) -> None:
        if res.status_code == 200:
            return
        error: ErrorResponse
        try:
            error = res.json()
        except:
            error = {"error": res.content.decode(errors="replace")}

        self._http_code_to_error(res.status_code, error)

    @staticmethod
    def _http_code_to_error(http_code, error) -> None:
        if http_code == 200:
            return
        if http_code == 400:
            raise InvalidArgumentError(error)
        elif http_code == 401:
            raise UnauthorizedError(error)
        elif http_code == 404:
            raise ObjectNotFoundError(error)
        elif http_code == 500:
            raise InternalServerError(error)
        else:
            raise HTTPError(error, http_code)

    def _db(self, method: str, *args: Any) -> Any:
        return self._post("/rpc/db", marshal([method, *args]))

    def _job(self, method: str, **kwargs: Any) -> Any:
        request_id = str(uuid.uuid4())
        return self._post("/rpc/job", marshal([method, kwargs, request_id]))

    def _lang(self, method: str, **kwargs: Any) -> Any:
        res = self._post("/rpc/lang", marshal(dict(method=method, params=kwargs)))
        ret = res["result"]
        if isinstance(ret, dict) and ret.get("error"):
            raise SessionError(ret["error"])
        return ret

    def _crawl_func(self, name: str, **kwargs: Any) -> Any:
        response = self._post("/rpc/crawl/func", marshal([name, kwargs]))
        return response

    def connect(
        self,
        chat_session_id: str,
        prompt_template_id: Optional[str] = None,
        open_timeout: int = 10,
        close_timeout: int = 10,
        max_connect_retries: int = 10,
        connect_retry_delay: int = 0.5,
        connect_retry_max_delay: int = 60,
    ) -> Session:
        """Create and participate in a chat session.

        This is a live connection to the H2OGPTE server contained to a specific
        chat session on top of a single collection of documents. Users will find all
        questions and responses in this session in a single chat history in the
        UI.

        Args:
            chat_session_id:
                ID of the chat session to connect to.
            prompt_template_id:
                ID of the prompt template to use.
            open_timeout:
                Timeout in seconds for opening the connection.
            close_timeout:
                Timeout in seconds for closing the connection.
            max_connect_retries:
                Maximum number of connection retry attempts.
            connect_retry_delay:
                Initial delay in seconds between connection retries.
            connect_retry_max_delay:
                Maximum delay in seconds between connection retries.

        Returns:
            Session: Live chat session connection with an LLM.

        """
        return Session(
            self._address,
            client=self,
            chat_session_id=chat_session_id,
            prompt_template_id=prompt_template_id,
            open_timeout=open_timeout,
            close_timeout=close_timeout,
            max_connect_retries=max_connect_retries,
            connect_retry_delay=connect_retry_delay,
            connect_retry_max_delay=connect_retry_max_delay,
        )


def _to_id(data: Dict[str, Any]) -> str:
    if data is not None and isinstance(data, dict) and data.get("error", ""):
        raise ValueError(data.get("error", ""))
    return Identifier(**data).id


def marshal(d):
    return json.dumps(d, allow_nan=False, separators=(",", ":"))
