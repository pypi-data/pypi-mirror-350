from django.conf import settings
import json
import logging
import time
import threading
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from foxsenseinnovations.vigil.vigil_utils.common_utils import mask_sensitive_data
from foxsenseinnovations.vigil.vigil_utils.api_monitoring_utils_django import (
    get_request_fields, get_response_fields, is_monitor_api
)
from foxsenseinnovations.vigil.vigil import Vigil
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiMonitoringOptions, MaskAttributes
from foxsenseinnovations.vigil.api_service_async import ApiServiceAsync
from foxsenseinnovations.vigil.constants.route_constants import RouteConstants

logger = logging.getLogger(__name__)
_thread_pool = ThreadPoolExecutor(max_workers=5)

class ApiMonitoringMiddleware:
    """
        ApiMonitoringMiddleware captures and monitors API requests and responses in a Django application.
        It utilizes the Vigil API monitoring system to record and analyze interactions, capturing details like
        headers, parameters, and timing. Integration provides insights for performance optimization and debugging.
        Middleware for monitoring API requests and responses asynchronously.
    """

    def __init__(self, get_response):
        """
        Initializes the ApiMonitoringMiddleware with the given get_response function.
        Args:
            get_response: A function to get the response for the request.
        Returns:
            None
        """
        self.get_response = get_response
        self.options = getattr(settings, 'API_MONITORING_OPTIONS', ApiMonitoringOptions())
        self.client_version = getattr(self.options, 'clientVersion', None) or Vigil.version
        self.exclude_patterns = getattr(self.options, "exclude", None)
        self.include_patters = getattr(self.options,"include",None)
        self.mask_attrs = getattr(self.options, "maskAttributes", MaskAttributes())

        self.instance_url = Vigil.instance_url
        self.api_monitoring_path = RouteConstants.API_MONITORING
        self.api_key = Vigil.api_key


    def __call__(self, request):
        request.original_body = getattr(request, 'body', None)

        path = request.path or request.get_full_path()
        method = request.method
        should_monitor = is_monitor_api(request, method, path, self.exclude_patterns,self.include_patters)

        start_time = datetime.now(timezone.utc).isoformat() if should_monitor else None

        response = self.get_response(request)

        if not should_monitor:
            return response

        end_time = datetime.now(timezone.utc).isoformat()

        # Submit the background task
        try:
            _thread_pool.submit(
            self._process_monitoring_data,
            request, response, start_time, end_time, path
        )
        except RuntimeError as e:
            logger.error(f"[Vigil] Failed to submit monitoring task: {e}", exc_info=True)

        return response


    def _process_monitoring_data(self, request, response, start_time, end_time, path):
        """Background worker to process monitoring data without delaying response"""
        try:

            # Get fields but minimize processing
            api_request = get_request_fields(request)
            api_response = get_response_fields(response)

            # Parse response body
            try:
                response_body = json.loads(api_response.responseBody) if api_response.responseBody else {}
            except json.JSONDecodeError:
                response_body = {"error": "Invalid JSON"}

            # Apply masks to sensitive data
            api_response.responseBody = mask_sensitive_data(response_body, self.mask_attrs.responseBody)
            api_response.responseHeaders = mask_sensitive_data(api_response.responseHeaders, self.mask_attrs.responseHeaders)

            # Build request data
            request_details = api_request.request_details
            request_data = {
                "host": api_request.host,
                "userAgent": request_details.get("userAgent", ""),
                "httpMethod": api_request.httpMethod,
                "cookies": request_details.get("cookies", {}),
                "ip": request_details.get("ip", ""),
                "headers": mask_sensitive_data(request_details.get("headers", {}), self.mask_attrs.requestHeaders),
                "requestBody": mask_sensitive_data(request_details.get("requestBody", {}), self.mask_attrs.requestBody),
                "protocol": request_details.get("protocol", ""),
                "hostName": request_details.get("hostName", ""),
                "url": api_request.url,
                "path": request_details.get("path", ""),
                "originalUrl": api_request.originalUrl,
                "baseUrl": api_request.baseUrl,
                "query": request_details.get("query", {}),
                "subDomains": request_details.get("subdomains", []),
                "uaVersionBrand": request_details.get("uaVersionBrand", ""),
                "uaMobile": request_details.get("uaMobile", False),
                "uaPlatform": request_details.get("uaPlatform", ""),
                "reqAcceptEncoding": request_details.get("reqAcceptEncoding", ""),
                "reqAcceptLanguage": request_details.get("reqAcceptLanguage", ""),
                "rawHeaders": mask_sensitive_data(request_details.get("rawHeaders", []), self.mask_attrs.requestHeaders),
                "httpVersion": api_request.httpVersion,
                "remoteAddress": request_details.get("remoteAddress", ""),
                "remoteFamily": request_details.get("remoteFamily", ""),
                "params": request_details.get("params", {}),
            }

            # Construct final data payload
            data = {
                "clientVersion": self.client_version,
                "startTime": start_time,
                "endTime": end_time,
                "request": request_data,
                "response": api_response.__dict__
            }

            # Call API directly without async/await
            ApiServiceAsync.send_monitoring_data(
                self.instance_url,
                self.api_monitoring_path,
                data,
                self.api_key
            )
            logger.info(f"[Vigil] API monitoring record created successfully for {data['request']['path']}")

        except Exception as e:
            logger.error(f"[Vigil] Error processing monitoring data: {e}", exc_info=True)