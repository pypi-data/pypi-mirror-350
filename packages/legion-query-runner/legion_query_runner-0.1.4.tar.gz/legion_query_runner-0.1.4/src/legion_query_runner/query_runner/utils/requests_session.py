import logging
from typing import Optional, Tuple, Union

import advocate
import requests
from advocate.exceptions import UnacceptableAddressException

logger = logging.getLogger(__name__)

# Use advocate for requests that might hit internal services
requests_or_advocate = advocate

# Create a session that uses advocate
requests_session = requests_or_advocate.Session()

def is_private_address(address: str) -> bool:
    """Check if an address is private."""
    try:
        return advocate.is_private_address(address)
    except Exception:
        return False

def is_acceptable_address(address: str) -> bool:
    """Check if an address is acceptable."""
    try:
        return advocate.is_acceptable_address(address)
    except Exception:
        return False 