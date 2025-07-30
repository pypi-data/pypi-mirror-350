from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import ClosingIterator
from foxsenseinnovations.vigil.vigil_utils.common_utils import mask_sensitive_data
from foxsenseinnovations.vigil.vigil_utils.api_monitoring_utils_flask import (
    get_request_fields,
    get_response_fields,
    is_monitor_api,
    generate_path,
)
from foxsenseinnovations.vigil.vigil import Vigil
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiMonitoringOptions, MaskAttributes
from foxsenseinnovations.vigil.api_service import ApiService
from foxsenseinnovations.vigil.constants.route_constants import RouteConstants
from datetime import datetime, timezone
from io import BytesIO
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(message)s')


class ApiMonitoringMiddleware:
    """
    Middleware for monitoring API requests and responses in a Flask application.
    Captures and analyzes headers, parameters, and response details.
    """

    def __init__(self, app, options=None):
        """
        Initializes the middleware with the Flask application and options.
        Args:
            app: The Flask application.
            options: API monitoring options.
        """
        self.app = app.wsgi_app
        self.url_map = app.url_map
        self.adapter = self.url_map.bind('')
        self.options = options or ApiMonitoringOptions()

    def extract_path_params(self, path_info, method):
        """
        Extracts path parameters dynamically using Flask's URL map.
        Args:
            path_info: The request path.
            method: The HTTP method of the request.
        Returns:
            dict: A dictionary of path parameters.
        """
        try:
            endpoint, args = self.adapter.match(path_info, method=method)
            return args
        except Exception:
            return {}

    def __call__(self, environ, start_response):
        try:
            """
            Handles incoming requests and outgoing responses.
            """
            start_time = datetime.now(timezone.utc).isoformat()
            request = Request(environ)
            monitor_api = is_monitor_api(
                request.method,
                request.path if request.path else request.full_path,
                getattr(self.options, "exclude", None),
                getattr(self.options, "include",None)
            )

            # Cache the raw request body
            raw_data = request.get_data(cache=True, parse_form_data=False)
            environ['wsgi.input'] = BytesIO(raw_data)

            # Custom start response to capture status code
            status_code_message = []

            def custom_start_response(status, headers, exc_info=None):
                status_code_message.append(status)
                return start_response(status, headers, exc_info)

            # Process the request
            app_iter = self.app(environ, custom_start_response)
            app_iter_list = list(app_iter)
            response = Response(app_iter_list, status=status_code_message[0])

            if monitor_api:
                end_time = datetime.now(timezone.utc).isoformat()
                api_request = get_request_fields(request)
                api_response = get_response_fields(response)
                path_params = self.extract_path_params(request.path, request.method)

                mask_attrs = getattr(self.options, "maskAttributes", MaskAttributes())

                request_data = {
                        "host": api_request.host,
                        "userAgent": api_request.request_details["userAgent"],
                        "httpMethod": api_request.httpMethod,
                        "cookies": api_request.request_details["cookies"],
                        "ip": api_request.request_details["ip"],
                        "headers": mask_sensitive_data(
                            api_request.request_details["headers"], 
                            mask_attrs.requestHeaders
                        ),
                        "requestBody": mask_sensitive_data(
                            api_request.request_details["requestBody"], 
                            mask_attrs.requestBody
                        ),
                        "protocol": api_request.request_details["protocol"],
                        "hostName": api_request.request_details["hostName"],
                        "url": api_request.url,
                        "path": api_request.request_details["path"],
                        "originalUrl": api_request.originalUrl,
                        "baseUrl": api_request.baseUrl,
                        "query": api_request.request_details["query"],
                        "subDomains": api_request.request_details["subdomains"],
                        "uaVersionBrand": api_request.request_details["uaVersionBrand"],
                        "uaMobile": api_request.request_details["uaMobile"],
                        "uaPlatform": api_request.request_details["uaPlatform"],
                        "reqAcceptEncoding": api_request.request_details["reqAcceptEncoding"],
                        "reqAcceptLanguage": api_request.request_details["reqAcceptLanguage"],
                        "rawHeaders": mask_sensitive_data(
                            api_request.request_details["rawHeaders"], 
                            mask_attrs.requestHeaders
                        ),
                        "httpVersion": api_request.httpVersion,
                        "remoteAddress": api_request.request_details["remoteAddress"],
                        "remoteFamily": api_request.request_details["remoteFamily"],
                        "params": path_params,  
                    }
                try:
                    response_body_dict = json.loads(api_response.responseBody) 
                except json.JSONDecodeError:
                    logging.info('Error while converting to json::')
                    raise 
                api_response.responseBody = mask_sensitive_data(response_body_dict, mask_attrs.responseBody)
                api_response.responseHeaders = mask_sensitive_data(api_response.responseHeaders, mask_attrs.responseHeaders)
                data = {
                    "clientVersion": self.options.clientVersion if self.options.clientVersion is not None else Vigil.version,
                    "startTime": start_time,
                    "endTime": end_time,
                    "request": request_data,
                    "response": api_response.__dict__
                }

                try:
                    ApiService.make_api_call(
                        Vigil.instance_url,
                        RouteConstants.API_MONITORING,
                        data,
                        Vigil.api_key,
                    )
                    logging.info(f"[Vigil] API monitoring record created successfully for the API - {generate_path(request.path or request.url, request.args)}")
                except Exception as err:
                    logging.error(f"[Vigil] Error while creating API monitoring record: {err}")

            # Return the response
            app_iter_rewind = iter(app_iter_list)
            return ClosingIterator(app_iter_rewind, response.close)
        except Exception as e:
            logging.error(f"[Vigil] Error while creating API monitoring record: {e}")
