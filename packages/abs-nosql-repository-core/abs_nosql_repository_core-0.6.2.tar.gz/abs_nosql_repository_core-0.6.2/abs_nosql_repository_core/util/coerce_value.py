from datetime import datetime
from functools import lru_cache
from typing import Any, Union, Dict, List

# Cache for datetime format parsing
@lru_cache(maxsize=128)
def parse_datetime(value: str) -> Union[datetime, str]:
    """
    Parse datetime string with caching for better performance.
    Supports multiple ISO 8601 formats.
    """
    formats = [
        "%Y-%m-%dT%H:%M:%S",       # e.g., 2025-05-10T14:00:00
        "%Y-%m-%dT%H:%M:%SZ",      # e.g., 2025-05-10T14:00:00Z
        "%Y-%m-%dT%H:%M:%S.%f",    # e.g., 2025-05-10T14:00:00.123456
        "%Y-%m-%dT%H:%M:%S.%fZ",   # e.g., 2025-05-10T14:00:00.123456Z
        "%Y-%m-%d"                 # e.g., 2025-05-10
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return value

# Cache for boolean string values
BOOLEAN_MAP = {
    "true": True, "yes": True, "1": True,
    "false": False, "no": False, "0": False,
    "null": None, "none": None, "": None
}

def coerce_value(value: Any) -> Any:
    """
    Coerce a value to its appropriate Python type.
    Handles nested structures (lists and dicts) recursively.
    Optimized for common cases and includes caching for better performance.
    """
    # Fast path for non-string types
    if not isinstance(value, str):
        if isinstance(value, list):
            return [coerce_value(item) for item in value]
        if isinstance(value, dict):
            return {k: coerce_value(v) for k, v in value.items()}
        return value

    # Fast path for empty string
    if not value:
        return value

    # Check boolean/null values first (most common case)
    lowered = value.lower()
    if lowered in BOOLEAN_MAP:
        return BOOLEAN_MAP[lowered]

    # Check for integers (common case)
    if value.isdigit():
        return int(value)

    # Check for floats
    try:
        return float(value)
    except ValueError:
        pass

    # Check for datetime (least common case)
    return parse_datetime(value)
