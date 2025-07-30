import httpx
import logging
import concurrent.futures
import threading
import time
from typing import Any, Dict, Optional
from functools import lru_cache

logger = logging.getLogger(__name__)

# Thread-local storage for client reuse
_thread_local = threading.local()

# Thread pool for background tasks
_thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)

class ApiServiceAsync:
    """
    ApiService is a utility class for making HTTP POST requests to external APIs. Its static method,
    make_api_call, constructs the API endpoint URL and sends a POST request with provided data and headers,
    including an API key for authorization. It abstracts away HTTP request complexity, leveraging the requests
    library, and offers a centralized interface for API interaction within applications.    """

    _timeout = httpx.Timeout(100.0)

    @staticmethod
    def get_client():
        """Get thread-local client for connection pooling"""
        if not hasattr(_thread_local, 'client'):
            _thread_local.client = httpx.Client(
                timeout=ApiServiceAsync._timeout,
                limits=httpx.Limits(max_keepalive_connections=10, max_connections=20)
            )
        return _thread_local.client

    @staticmethod
    @lru_cache(maxsize=100)
    def build_url(base_url: str, api_url: str) -> str:
        """Build and cache the URL to avoid string operations"""
        if base_url.endswith('/') and api_url.startswith('/'):
            return base_url + api_url[1:]
        elif not base_url.endswith('/') and not api_url.startswith('/'):
            return base_url + '/' + api_url
        else:
            return base_url + api_url

    @classmethod
    async def make_api_call(
        cls,
        base_url: str,
        api_url: str,
        data: Dict[str, Any],
        api_key: str
    ) -> Optional[Dict[str, Any]]:
        """Make an async API call with optimized client configuration"""
        url = cls.build_url(base_url, api_url)
        headers = {"x-api-key": api_key, "Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=cls._timeout) as client:
            try:
                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
                return None

            except Exception as e:
                logger.error(f"API call error: {str(e)}")
                return None

    @classmethod
    def send_monitoring_data(
        cls,
        base_url: str,
        api_url: str,
        data: Dict[str, Any],
        api_key: str
    ) -> None:
        """
        Non-blocking method to send monitoring data in background
        """
        # Submit to thread pool and don't wait for result
        _thread_pool.submit(
            cls._send_monitoring_data_sync,
            base_url,
            api_url,
            data,
            api_key
        )

    @classmethod
    def _send_monitoring_data_sync(
        cls,
        base_url: str,
        api_url: str,
        data: Dict[str, Any],
        api_key: str
    ) -> None:
        """
        Synchronous implementation to send monitoring data
        """
        url = cls.build_url(base_url, api_url)
        headers = {"x-api-key": api_key, "Content-Type": "application/json"}

        try:
            client = cls.get_client()
            response = client.post(url, json=data, headers=headers, timeout=cls._timeout)
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Error {e.response.status_code}")

        except Exception as e:
            logger.error(f"Error sending monitoring data: {str(e)}")