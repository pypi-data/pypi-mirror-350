from typing import Any, Dict, List
import re

class MaskOptions:
    """
    MaskOptions is used to define options for masking sensitive data in API requests.
    Attributes:
        mask_with (str): The character used for masking sensitive data.
        fields (List[str]): List of fields to be masked.
        prefixes (List[str]): List of prefixes of fields to be masked.
    """
    def __init__(self, mask_with: str, fields: List[str], prefixes: List[str]) -> None:
        self.mask_with = mask_with
        self.fields = fields
        self.prefixes = prefixes

def mask_data(data: Dict[str, Any], mask_options: MaskOptions) -> Dict[str, Any]:
    """
    Mask sensitive data in the provided dictionary based on the given MaskOptions.
    Args:
        data (Dict[str, Any]): The dictionary containing data to be masked.
        mask_options (MaskOptions): Options for masking sensitive data.
    Returns:
        Dict[str, Any]: The dictionary with sensitive data masked.
    """
    for key in data.keys():
        if key in mask_options.fields or any(key.startswith(prefix) for prefix in mask_options.prefixes):
            data[key] = mask_options.mask_with * 5
    return data

def mask_sensitive_data(data, mask_keys, mask_char="*", reveal_start=2, reveal_end=2):
    """
    Masks specified keys in the given data, supporting dictionaries, lists, and primitive types.
    
    Args:
        data: The data to process (can be a dict, list, or primitive value).
        mask_keys: A list of keys to apply masking to (for dicts).
        mask_char: Character to use for masking.
        reveal_start: Number of characters to reveal from the start.
        reveal_end: Number of characters to reveal from the end.
    
    Returns:
        The data with sensitive fields masked.
    """
    if isinstance(data, dict):
        masked_data = {}
        for key, value in data.items():
            if key in mask_keys:
                if isinstance(value, str):
                    masked_data[key] = mask_value(value, mask_char, reveal_start, reveal_end)
                elif isinstance(value, (int, float)):
                    masked_data[key] = mask_value(str(value), mask_char, reveal_start, reveal_end)
                else:
                    masked_data[key] = mask_char * 5
            else:
                masked_data[key] = mask_sensitive_data(value, mask_keys, mask_char, reveal_start, reveal_end)
        return masked_data
    
    elif isinstance(data, list):
        return [mask_sensitive_data(item, mask_keys, mask_char, reveal_start, reveal_end) for item in data]
    elif isinstance(data, tuple):
        if len(data)==2 and data[0] in mask_keys:
            return (data[0], mask_value(data[1]))
        else:
            return data
    return data


def mask_value(value, mask_char="*", reveal_start=2, reveal_end=2):
    """
    Masks a single value (string) while partially revealing it.
    
    Args:
        value: The value to mask (string or primitive).
        mask_char: Character to use for masking.
        reveal_start: Number of characters to reveal from the start.
        reveal_end: Number of characters to reveal from the end.
    
    Returns:
        Masked value (string).
    """
    if not isinstance(value, str):
        return value

    length = len(value)
    
    if length <= reveal_start + reveal_end:
        reveal_start = max(1, length // 2)
        reveal_end = length - reveal_start

    masked_section = mask_char * (length - reveal_start - reveal_end)
    return f"{value[:reveal_start]}{masked_section}{value[-reveal_end:]}"


def mask_number(value, mask_char="*", reveal_digits=4):
    """
    Masks all but the last `reveal_digits` digits of a number, while showing the last 4 digits.
    
    Args:
        value: The number (int or float) to mask.
        mask_char: Character to use for masking (default is "*").
        reveal_digits: Number of digits to reveal from the end.
    
    Returns:
        Masked number (string).
    """
    if isinstance(value, (int, float)):
        value_str = str(value)
        if len(value_str) <= reveal_digits:
            return value_str 
        masked_section = mask_char * (len(value_str) - reveal_digits)
        return f"{masked_section}{value_str[-reveal_digits:]}"
    return value


def generate_path(path: str, params: dict) -> str:
    """
    Generate a path with substituted parameters.
    Args:
        path (str): The original path containing placeholders.
        params (dict): Dictionary containing parameter values for substitution.
    Returns:
        str: The generated path with substituted parameters.
    """
    # Use regular expression to find placeholders in the path
    placeholders = re.findall(r'<([^>]+)>', path)
    if len(placeholders)==len(params):
      # Replace placeholders with corresponding values from params
      for i, placeholder in enumerate(placeholders):
          parts = placeholder.split(':')
          placeholder_name = parts[-1]  # Take the last part after the colon

          if placeholder_name in params:
              path = path.replace(f'<{placeholder}>', str(params[placeholder_name]))
              placeholders[i] = placeholder_name  # Update the list with the correct placeholder name

    return path