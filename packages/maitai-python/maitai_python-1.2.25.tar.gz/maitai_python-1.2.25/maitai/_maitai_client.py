import concurrent.futures
import os

import httpx

from maitai_common.version import version

# Common client settings to ensure consistency
CLIENT_SETTINGS = {
    "http2": True,
    "limits": httpx.Limits(
        max_keepalive_connections=200,
        max_connections=1000,
    ),
    "timeout": httpx.Timeout(timeout=600, connect=5.0),
    "follow_redirects": True,
}

# In _base_client.py, they define DEFAULT_MAX_RETRIES = 2
# We'll incorporate that into our transport settings
DEFAULT_MAX_RETRIES = 2


def _get_aws_instance_metadata(url, timeout=2):
    try:
        token_url = "http://169.254.169.254/latest/api/token"
        token_headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        with httpx.Client() as client:
            token_response = client.put(
                token_url, headers=token_headers, timeout=timeout
            )

            if token_response.status_code == 200:
                token = token_response.text
                headers = {"X-aws-ec2-metadata-token": token}
            else:
                headers = None

            response = client.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
    except Exception:
        return None


def _determine_maitai_host():
    if maitai_host := os.environ.get("MAITAI_HOST"):
        return maitai_host.rstrip("/")

    if (
        _get_aws_instance_metadata(
            "http://169.254.169.254/latest/meta-data/placement/region"
        )
        == "us-west-2"
    ):
        return "https://api.aws.us-west-2.trymaitai.ai"

    return "https://api.trymaitai.ai"


class MaitaiClient:
    _client = None
    _async_client = None
    maitai_host = _determine_maitai_host()

    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor()

    def get_client(self):
        if self._client is None:
            self._client = httpx.Client(
                **CLIENT_SETTINGS,
                transport=httpx.HTTPTransport(retries=DEFAULT_MAX_RETRIES, http2=True),
            )
        return self._client

    async def get_async_client(self):
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                **CLIENT_SETTINGS,
                transport=httpx.AsyncHTTPTransport(
                    retries=DEFAULT_MAX_RETRIES, http2=True
                ),
            )
        return self._async_client

    def cleanup(self):
        try:
            self.executor.shutdown()
        except Exception:
            pass
        try:
            self.close_client()
        except Exception:
            pass

    def close_client(self):
        if self._client:
            self._client.close()
            self._client = None

    async def close_async_client(self):
        if self._async_client:
            await self._async_client.aclose()
            self._async_client = None

    def __del__(self):
        self.cleanup()

    def log_error(self, api_key: str, error: str, path: str):
        self.executor.submit(self._log_error, api_key, error, path)

    def _log_error(self, api_key: str, error: str, path: str):
        host = self.maitai_host
        if "/batch" in host:
            host = host.replace("/batch", "")
        url = f"{host}/metrics/increment/python_sdk_error"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "User-Agent": version,
        }
        labels = {
            "cause": error,
            "type": "ERROR",
            "path": path,
        }
        try:
            client = self.get_client()
            return client.put(url, headers=headers, json=labels)
        except:
            pass

    async def log_error_async(self, api_key: str, error: str, path: str):
        host = self.maitai_host
        if "/batch" in host:
            host = host.replace("/batch", "")
        url = f"{host}/metrics/increment/python_sdk_error"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "User-Agent": version,
        }
        labels = {
            "cause": error,
            "type": "ERROR",
            "path": path,
        }
        try:
            client = await self.get_async_client()
            return await client.put(url, headers=headers, json=labels)
        except:
            pass

    def init_sdk(self, api_key: str, host: str):
        """Initialize the SDK and warm up connections."""
        if "/batch" in host:
            host = host.replace("/batch", "")
        url = f"{host}/config/init_sdk"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "User-Agent": version,
        }

        # Get the shared client to warm up connections
        client = self.get_client()
        response = client.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            raise Exception(f"Failed to initialize Maitai client: {response.text}")
        return response.json()
