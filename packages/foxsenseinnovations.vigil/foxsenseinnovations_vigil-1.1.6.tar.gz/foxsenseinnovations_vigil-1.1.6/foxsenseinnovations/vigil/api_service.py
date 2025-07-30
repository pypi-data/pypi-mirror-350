from typing import Any, Dict, Optional
import requests
import logging
import threading
import time
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

_thread_local = threading.local()

_thread_pool = ThreadPoolExecutor(max_workers=5)

class ApiService:
    """
    ApiService is a utility class for making HTTP POST requests to external APIs. Its static method,
    make_api_call, constructs the API endpoint URL and sends a POST request with provided data and headers,
    including an API key for authorization. It abstracts away HTTP request complexity, leveraging the requests
    library, and offers a centralized interface for API interaction within applications.    """

    _timeout = 100.0

    @staticmethod
    def get_session():
        """Get thread-local session for connection pooling"""
        if not hasattr(_thread_local, 'session'):
            _thread_local.session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=20,
                pool_maxsize=100,
                max_retries=1
            )
            _thread_local.session.mount('http://', adapter)
            _thread_local.session.mount('https://', adapter)
        return _thread_local.session

    @staticmethod
    @lru_cache(maxsize=100)
    def build_url(base_url: str, api_url: str) -> str:
        """Build and cache URL to avoid string operations"""
        if base_url.endswith('/') and api_url.startswith('/'):
            return base_url + api_url[1:]
        elif not base_url.endswith('/') and not api_url.startswith('/'):
            return base_url + '/' + api_url
        else:
            return base_url + api_url

    @classmethod
    def make_api_call(
        cls,
        base_url: str,
        api_url: str,
        data: Dict[str, Any],
        api_key: str
    ) -> Optional[requests.Response]:
        """Make a synchronous API call with optimized parameters"""
        url = cls.build_url(base_url, api_url)
        headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        }

        try:
            session = cls.get_session()
            response = session.post(
                url,
                json=data,
                headers=headers,
                timeout=cls._timeout
            )
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
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
        # Submit to thread pool without waiting for result
        _thread_pool.submit(
            cls.make_api_call,
            base_url,
            api_url,
            data,
            api_key
        )