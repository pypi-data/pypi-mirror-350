import json
from datetime import datetime, date
from decimal import Decimal
from typing import Any

def json_dumps(data: Any) -> str:
    """
    JSON encoder function that handles Python data types that
    are not JSON serializable by default.
    
    Args:
        data: The data to encode to JSON
        
    Returns:
        str: JSON encoded string
    """
    def handler(obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif hasattr(obj, '__str__'):
            return str(obj)
        raise TypeError(f'Object of type {type(obj)} is not JSON serializable')

    return json.dumps(data, default=handler) 