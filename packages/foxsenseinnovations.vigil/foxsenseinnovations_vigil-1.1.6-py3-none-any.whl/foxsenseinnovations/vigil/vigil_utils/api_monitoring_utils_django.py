from typing import Any, Dict, Optional
from django.http import QueryDict
from django.urls import resolve
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiRequest, ApiResponse, ExcludeOptions, RequestDetails,IncludeOptions
from foxsenseinnovations.vigil.enums.http_method_enum import HttpMethod
from foxsenseinnovations.vigil.vigil_utils.common_utils import MaskOptions, mask_data, generate_path
import json
import re
import base64
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
def serialize_file(file):
    """
    Serialize file data for API consumption.
    Args:
        file: The file object to serialize.
    Returns:
        Dict[str, Any]: The serialized file data.
    """
    file_content = file.read()
    try:
        file_content = file_content.decode('utf-8')
    except UnicodeDecodeError:
        file_content = base64.b64encode(file_content).decode('utf-8')
    return {
        'filename': file.name,
        'content': file_content,
    }

def parse_multipart_body(request):
    """
    Parse multipart request body and extract data.
    Args:
        request: The HTTP request object.
    Returns:
        Dict[str, Any]: Parsed data from the request body.
    """
    data = dict(request.POST)
    files_data = {key: serialize_file(file) for key, file in request.FILES.items()}
    data.update(files_data)
    return data

def is_empty(request):
    """
    Check if an HTTP request is empty (contains no body, POST data, or files).
    Args:
        request: The HTTP request object.
    Returns:
        bool: True if the request is empty, False otherwise.
    """
    if (not request.body) and len(request.POST)==0 and len(request.FILES)==0:
        return True
    else:
        return False

def extract_path_params(request):
    """
    Extract path parameters from an HTTP request.
    Args:
        request: The HTTP request object.
    Returns:
        dict: Dictionary containing path parameters extracted from the request.
    """
    resolved = resolve(request.path_info)
    request.path_params = resolved.kwargs
    return request.path_params

def get_request_fields(request: Any) -> ApiRequest:
    """
    Extract relevant fields from an HTTP request for API monitoring.
    Args:
        request (Any): The HTTP request object.
    Returns:
        ApiRequest: An object containing relevant fields extracted from the request.
    """
    mask_options = MaskOptions(mask_with='*', fields=['authorization'], prefixes=['x-'])

    def get_request_body(request: Any) -> Optional[Dict[str, Any]]:
        """
        Extract the request body from an HTTP request.
        Args:
            request (Any): The HTTP request object.
        Returns:
            Optional[Dict[str, Any]]: The parsed request body as a dictionary, or None if the request body
            is empty or cannot be parsed.
        """
        content_type = request.headers.get('Content-Type', '')
        if is_empty(request):
            return None
        else:
            if content_type.startswith('application/json'):
                try:
                    # Parse the byte string directly without decoding
                    json_data = json.loads(request.body)
                    return json_data
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON: {e}")
                    return {}
            elif content_type.startswith('application/x-www-form-urlencoded'):
                return QueryDict(request.body.decode('utf-8'))
            elif content_type.startswith('multipart/form-data'):
                return parse_multipart_body(request)
            else:
                decoded_raw_body = request.body.decode('utf-8')
                if (decoded_raw_body == ""):
                    return {}
                return {'raw_body': decoded_raw_body}

    request_details = RequestDetails(
        headers=mask_data(dict(request.headers), mask_options),
        userAgent=request.headers.get('user-agent'),
        cookies = {},  
        ip=request.META.get('REMOTE_ADDR'),
        requestBody=get_request_body(request),
        protocol=request.scheme,
        hostName=request.META.get('HTTP_HOST'),
        query=dict(request.GET),
        subdomains=[] if request.META.get('HTTP_HOST', '').count('.') == 3 else request.META.get('HTTP_HOST', '').split('.')[:-2],
        uaVersionBrand=request.headers.get('sec-ch-ua'),
        uaMobile=request.headers.get('sec-ch-ua-mobile'),
        uaPlatform=request.headers.get('sec-ch-ua-platform'),
        reqAcceptEncoding=request.headers.get('accept-encoding'),
        reqAcceptLanguage=request.headers.get('accept-language'),
        rawHeaders=list(request.headers.items()),
        remoteAddress=request.META.get('REMOTE_ADDR'),
        remoteFamily=request.META.get('REMOTE_FAMILY', None),
        path=request.path or request.get_full_path(),
        params=extract_path_params(request)
    )

    return ApiRequest(
        host=request.headers.get('host'),
        httpMethod=request.method,
        url=request.build_absolute_uri(),
        originalUrl=request.build_absolute_uri(),
        baseUrl=request.build_absolute_uri('/')[:-1],
        httpVersion=int(round(float(request.META.get('SERVER_PROTOCOL', 'HTTP/1.0').split('/')[-1]))),
        request_details=request_details
    )

def get_response_fields(response: Any) -> ApiResponse:
    """
    Extract relevant fields from an HTTP response for API monitoring.
    Args:
        response (Any): The HTTP response object.
    Returns:
        ApiResponse: An object containing relevant fields extracted from the response.
    """
    return ApiResponse(
        responseStatusCode=response.status_code,
        responseStatusMessage=response.reason_phrase,
        responseBody=response.content.decode('utf-8'),
        responseHeaders=dict(response.items())
    )

def is_monitor_api(request: Any, method: HttpMethod, path: str, exclude_options: Optional[ExcludeOptions] = None,include_options: Optional[IncludeOptions] = None) -> bool:
    """
   Check if an API endpoint should be monitored based on inclusion and exclusion options.
    
        Args:
            method (HttpMethod): The HTTP method of the request.
            path (str): The path of the API endpoint.
            exclude_options (Optional[ExcludeOptions]): Options for excluding certain API endpoints from monitoring
            (default None).
            include_options (Optional[IncludeOptions]): Options for including only specific API endpoints in monitoring
            (default None).
    
        Returns:
            bool: True if the API endpoint should be monitored, False otherwise.
        
        Notes:
            - If both exclude_options and include_options are None, all APIs will be monitored.
            - When both are provided, exclusion is checked first, then inclusion.
            - If only include_options is provided, only the specified paths will be monitored.
            - If only exclude_options is provided, all paths except the excluded ones will be monitored.
    """
    monitor_api = True
    if exclude_options is None and include_options is None:
        return monitor_api
    monitor_api = not check_path_excluded(request,method,path,exclude_options)
    if(monitor_api):
        monitor_api = check_path_included(request,method,path,include_options)
    return monitor_api


def check_path_excluded(request: Any, method: HttpMethod, path: str, exclude_options: Optional[ExcludeOptions] = None) -> bool:
    if not exclude_options or method not in exclude_options.__dict__ or not exclude_options.__dict__[method]:
        return False
    exclude_paths = exclude_options.__dict__[method]
    for exclude_path in exclude_paths:
        params = extract_path_params(request)
        if (params and path == generate_path(exclude_path, params)) or path == exclude_path:
            return True

        elif is_regex_pattern(exclude_path):
            try:
                regex = re.compile(exclude_path)
                if regex.match(path):
                    return True
            except Exception as e:
                logging.error(f"[Vigil] Invalid regex in exclude options : {e}, Exclude Path: {exclude_path}", exc_info=True)


def check_path_included(request : Any,method: HttpMethod, path: str,include_options: Optional[IncludeOptions] = None) -> bool:
    if not include_options or method not in include_options.__dict__ or not include_options.__dict__[method]:
        return True

    include_paths = include_options.__dict__[method]
    if len(include_paths) > 0:
        is_included = False

        for include_path in include_paths:
            params = extract_path_params(request)
            if (params and path == generate_path(include_path, params)) or path == include_path:
                is_included = True
                break
            elif is_regex_pattern(include_path):
                try:
                    regex = re.compile(include_path)
                    if regex.match(path):
                        is_included = True
                        break
                except Exception as e:
                    logging.error(f"[Vigil] Invalid regex in include options : {e}, Include Path: {include_path}", exc_info=True)
        return is_included
    return True




def is_regex_pattern(str_pattern : str) -> bool :
    if str_pattern.startswith('^') or str_pattern.endswith('$'):
        return True
    
    # Check for regex character combinations that wouldn't appear in URLs
    strong_regex_indicators = [
        r'\.\*', r'\.\+', r'\.\?', r'\\\w', r'\[.+?\]',
        r'\(.+?\)', r'\|', r'\{\d+,?\d*\}'
    ]
    
    for pattern in strong_regex_indicators:
        if re.search(pattern, str_pattern):
            return True
    
    # If a dot is not part of a version number, file extension, or domain name
    common_url_patterns = [
        r'\.\w{2,4}(?:\/|$)', 
        r'\/v\d+\.\d+\/',  
        r'\w+\.\w+\.\w+' 
    ]
    
    for pattern in common_url_patterns:
        if re.search(pattern, str_pattern):
            return False
    
    # If we have a standalone dot or plus not in the contexts above
    suspicious_patterns = [
        r'(?<!\w)\.(?!\w)',
        r'(?<!\w)\+(?!\w)'
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, str_pattern):
            return True
    
    # Fallback - if it has other regex characters, assume it's regex
    return bool(re.search(r'[{}\[\]\\^]', str_pattern))