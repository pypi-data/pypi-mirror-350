"""
OKX API client utilities for authentication and request handling.
"""

import httpx
import base64
import hmac
import hashlib
import json
from datetime import datetime
from typing import Any, Dict, Optional

from .constants import (
    OKX_API_BASE, OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE, 
    OKX_PROJECT_ID, OKX_SANDBOX, USER_AGENT
)


def create_okx_signature(timestamp: str, method: str, request_path: str, body: str = "") -> str:
    """Create OKX API signature using HMAC-SHA256."""
    if not OKX_SECRET_KEY:
        return ""
    
    # Ensure body is properly formatted JSON string if it's not empty
    if body and isinstance(body, (dict, list)):
        body = json.dumps(body, separators=(',', ':'))
    
    message = timestamp + method + request_path + body
    signature = base64.b64encode(
        hmac.new(
            OKX_SECRET_KEY.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
    ).decode('utf-8')
    
    return signature


def get_okx_headers(method: str, request_path: str, body: str = "") -> Dict[str, str]:
    """Generate OKX API headers with authentication."""
    # Generate current timestamp in the exact format OKX expects (ISO format with milliseconds)
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Add authentication headers if API credentials are available
    if OKX_API_KEY and OKX_SECRET_KEY and OKX_PASSPHRASE:
        signature = create_okx_signature(timestamp, method, request_path, body)
        headers.update({
            "OK-ACCESS-KEY": OKX_API_KEY,
            "OK-ACCESS-SIGN": signature,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": OKX_PASSPHRASE
        })
        
        # Add project ID if available
        if OKX_PROJECT_ID:
            headers["OK-ACCESS-PROJECT"] = OKX_PROJECT_ID
        
        if OKX_SANDBOX:
            headers["x-simulated-trading"] = "1"
    
    return headers


async def make_okx_request(url: str, method: str = "GET", body: Any = None) -> Optional[Dict[str, Any]]:
    """Make a request to the OKX API with proper authentication."""
    try:
        # Extract request path from full URL
        request_path = url.replace(OKX_API_BASE, "")
        
        # Convert body to JSON string if it's a dict/list
        body_str = ""
        if body is not None:
            if isinstance(body, (dict, list)):
                body_str = json.dumps(body, separators=(',', ':'))
            else:
                body_str = str(body)
        
        headers = get_okx_headers(method, request_path, body_str)
        
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            else:
                response = await client.request(
                    method, 
                    url, 
                    headers=headers, 
                    content=body_str if body_str else None, 
                    timeout=30.0
                )
            
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"OKX API Error: {e}")
        return None 