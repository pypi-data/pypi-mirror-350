import hashlib
import json
from typing import Any, Dict, Union

def gen_query_hash(query_text: str) -> str:
    """Generate a hash for a query text."""
    return hashlib.sha256(query_text.encode("utf-8")).hexdigest()

def json_loads(s: Union[str, bytes]) -> Dict[str, Any]:
    """Load JSON string or bytes into a Python object."""
    if isinstance(s, bytes):
        s = s.decode("utf-8")
    return json.loads(s) 