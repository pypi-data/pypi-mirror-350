from typing import Any, Dict, Optional, List
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiRequest, ApiResponse, ExcludeOptions, RequestDetails,IncludeOptions
from foxsenseinnovations.vigil.vigil_utils.common_utils import MaskOptions, mask_data, generate_path
from collections import defaultdict
import re
import base64
import logging
from http import HTTPStatus
from fastapi import Request
import socket

logging.basicConfig(level=logging.INFO, format='%(message)s')

def serialize_file(file):
    """
    Serialize file data for API consumption.
    Args:
        file: The file object to serialize.
    Returns:
        Dict[str, Any]: The serialized file data.
    """
    file_content = file.file.read()
    try:
        file_content = file_content.decode('utf-8')
    except UnicodeDecodeError:
        file_content = base64.b64encode(file_content).decode('utf-8')
    return {
        'filename': file.filename,
        'content': file_content,
    }

async def parse_multipart_body(request: Request) -> Dict[str, Any]:
    try:
        """
        Parse multipart request body and extract data.
        Args:
            request: The HTTP request object.
        Returns:
            Dict[str, Any]: Parsed data from the request body.
        """
        form_data = await request.form()
        files_data = {key: serialize_file(file) for key, file in form_data.items() if hasattr(file, 'file')}
        data = {key: value for key, value in form_data.items() if not hasattr(value, 'file')}
        data.update(files_data)
        return data
    except Exception as e:
        logging.error(f"[Vigil] Error while parsing multipart body: {e}")
        raise

def extract_subdomains(request: Request) -> List[str]:
    try:
        """
        Extract subdomains from the request host.
        
        Args:
            request (Request): FastAPI request object
        
        Returns:
            List[str]: List of subdomains
        
        Example:
            For host 'api.dev.example.com':
            Returns ['api', 'dev']
        """
        host = request.headers.get('host', '')
        if not host:
            return []
        
        # Remove port if present
        host = host.split(':')[0]
        
        # Split the host into parts
        parts = host.split('.')
        
        # Remove TLD and domain name (last two parts)
        # Only return parts if we have more than 2 parts (indicating subdomains exist)
        if len(parts) > 2:
            return parts[:-2]
        return []
    except Exception as e:
            logging.error(f"[Vigil] Error while extracting subdomains: {e}")
            raise

def get_remote_family(request: Request) -> Optional[str]:
    """
    Determine the remote address family (IPv4 or IPv6).
    
    Args:
        request (Request): FastAPI request object
    
    Returns:
        Optional[str]: 'IPv4', 'IPv6', or None if cannot be determined
    """
    client_host = request.client.host if request.client else None
    if not client_host:
        return None
    
    try:
        # Try to create an IP address object
        ip_addr = socket.inet_pton(socket.AF_INET, client_host)
        return 'IPv4'
    except socket.error:
        try:
            ip_addr = socket.inet_pton(socket.AF_INET6, client_host)
            return 'IPv6'
        except socket.error:
            return None

async def get_request_body(request: Request) -> Optional[Dict[str, Any]]:
    try:
        """
        Extract the request body from an HTTP request.
        Args:
            request (Request): The HTTP request object.
        Returns:
            Optional[Dict[str, Any]]: The parsed request body as a dictionary, or None if the request body is empty or cannot be parsed.
        """
        content_type = request.headers.get('content-type', '')
        if not request.body:
            return None
        else:
            if content_type.startswith('application/json'):
                try:
                    return await request.json()
                except Exception as e:
                    logging.error(f"Error decoding JSON: {e}")
                    return {}
            elif content_type.startswith('application/x-www-form-urlencoded'):
                return dict(await request.form())
            elif content_type.startswith('multipart/form-data'):
                return await parse_multipart_body(request)
            else:
                raw_body = await request.body()
                decoded_raw_body = raw_body.decode('utf-8')
                if (decoded_raw_body == ""):
                    return {}
                return {'raw_body': decoded_raw_body}
    except Exception as e:
        logging.error(f"[Vigil] Error while extracting the request body: {e}")
        raise

async def get_request_fields(request: Request) -> ApiRequest:
    try:
        """
        Extract relevant fields from an HTTP request for API monitoring.
        Args:
            request (Request): The HTTP request object.
        Returns:
            ApiRequest: An object containing relevant fields extracted from the request.
        """
        mask_options = MaskOptions(mask_with='*', fields=['authorization'], prefixes=['x-'])

        query_params = defaultdict(list)
        for key, value in request.query_params._list:
            query_params[key].append(value)

        request_details = RequestDetails(
            headers=mask_data(dict(request.headers), mask_options),
            userAgent=request.headers.get('user-agent'),
            cookies = {},
            ip=request.client.host if request.client else None,
            requestBody=await get_request_body(request),
            protocol=request.scope.get('scheme'),
            hostName=request.headers.get('host'),
            query=dict(query_params),
            subdomains=extract_subdomains(request),
            uaVersionBrand=request.headers.get('sec-ch-ua'),
            uaMobile=request.headers.get('sec-ch-ua-mobile'),
            uaPlatform=request.headers.get('sec-ch-ua-platform'),
            reqAcceptEncoding=request.headers.get('accept-encoding'),
            reqAcceptLanguage=request.headers.get('accept-language'),
            rawHeaders=list(request.headers.items()),
            remoteAddress=request.client.host if request.client else None,
            remoteFamily=get_remote_family(request),
            path=request.url.path,
            params=dict(request.path_params)
        )

        return ApiRequest(
            host=request.headers.get('host'),
            httpMethod=request.method,
            url=str(request.url),
            originalUrl=str(request.url),
            baseUrl=request.base_url._url,
            httpVersion=int(round(float(request.scope.get('http_version', '1.1')))),
            request_details=request_details
        )
    except Exception as e:
        logging.error(f"[Vigil] Error while extracting request fields: {e}")
        raise

def get_response_fields(response) -> ApiResponse:
    try:
        """
        Extract relevant fields from an HTTP response for API monitoring.
        Args:
            response (Response): The HTTP response object.
        Returns:
            ApiResponse: An object containing relevant fields extracted from the response.
        """
        try:
            decoded_body = response.body.decode('utf-8')
        except UnicodeDecodeError:
            import base64
            decoded_body = base64.b64encode(response.body).decode('utf-8')
        return ApiResponse(
            responseStatusCode=response.status_code,
            responseStatusMessage=HTTPStatus(response.status_code).phrase,
            responseBody=decoded_body,
            responseHeaders=dict(response.headers)
        )
    except Exception as e:
            logging.error(f"[Vigil] Error while extracting response fields: {e}")
            raise

def extract_path_params(pattern: str, actual_path: str) -> Optional[Dict[str, str]]:
    try:
        """
        Extract path parameters from an actual path based on a pattern.
        
        Args:
            pattern (str): The pattern with parameter placeholders (e.g., "/details/{param}/the/plan/{ply}")
            actual_path (str): The actual path (e.g., "/details/123/the/plan/456")
        
        Returns:
            Optional[Dict[str, str]]: Dictionary of parameter names and values, or None if path doesn't match pattern
        """
        # Convert pattern to regex
        regex_pattern = pattern.replace("/", "\\/")
        regex_pattern = re.sub(r'\{([^}]+)\}', r'(?P<\1>[^/]+)', regex_pattern)
        regex_pattern = f"^{regex_pattern}$"
        
        # Try to match the path
        match = re.match(regex_pattern, actual_path)
        if match:
            return match.groupdict()
        return None
    except Exception as e:
        logging.error(f"[Vigil] Error while extracting path params: {e}")
        raise

def normalize_path(path: str) -> str:
    try:
        """
        Normalize a path by removing trailing slashes and ensuring leading slash.
        
        Args:
            path (str): Path to normalize
        
        Returns:
            str: Normalized path
        """
        # Remove trailing slashes and ensure leading slash
        path = path.rstrip('/')
        if not path.startswith('/'):
            path = '/' + path
        return path
    except Exception as e:
        logging.error(f"[Vigil] Error while normalizing path: {e}")
        raise

def paths_match(exclude_path: str, actual_path: str) -> bool:
    try:
        """
        Check if an actual path matches an exclusion pattern.
        
        Args:
            exclude_path (str): The exclusion pattern (may contain parameters)
            actual_path (str): The actual path to check
        
        Returns:
            bool: True if paths match, False otherwise
        """
        # Normalize both paths
        exclude_path = normalize_path(exclude_path)
        actual_path = normalize_path(actual_path)
        
        # If paths are identical, they match
        if exclude_path == actual_path:
            return True
        
        # Check if exclude_path has parameters
        if '{' in exclude_path:
            params = extract_path_params(exclude_path, actual_path)
            return params is not None
        
        return False
    except Exception as e:
        logging.error(f"[Vigil] Error while matching paths: {e}")
        raise

def is_monitor_api(method: str, path: str, exclude_options: Optional[ExcludeOptions] = None,include_options: Optional[IncludeOptions] = None) -> bool:
    try:
        """
       Check if an API endpoint should be monitored based on inclusion and exclusion options.
    
        Args:
            method (str): The HTTP method of the request.
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
            
        # Get excluded routes for the method (case-insensitive)
        method = method.upper()
        monitor_api = not check_path_excluded(method,path,exclude_options)

        if(monitor_api):
            monitor_api = check_path_included(method,path, include_options)
        return monitor_api
    except Exception as e:
        logging.error(f"[Vigil] Error while checking to monitor API: {e}")
        raise

def check_path_excluded(method: str, path: str, exclude_options: Optional[ExcludeOptions] = None) -> bool:
    if not exclude_options or method not in exclude_options.__dict__ or not exclude_options.__dict__[method]:
        return False
    exclude_paths = exclude_options.__dict__[method]
    for exclude_path in exclude_paths:
        if paths_match(exclude_path,path):
            return True

        elif is_regex_pattern(exclude_path):
            try:
                regex = re.compile(exclude_path)
                if regex.match(path):
                    return True
            except Exception as e:
                logging.error(f"[Vigil] Invalid regex in exclude options : {e}, Exclude Path: {exclude_path}", exc_info=True)

def check_path_included(method: str, path: str,include_options: Optional[IncludeOptions] = None) -> bool:
    if not include_options or method not in include_options.__dict__ or not include_options.__dict__[method]:
        return True

    include_paths = include_options.__dict__[method]
    if len(include_paths) > 0:
        is_included = False

        for include_path in include_paths:
            if paths_match(include_path,path):
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
