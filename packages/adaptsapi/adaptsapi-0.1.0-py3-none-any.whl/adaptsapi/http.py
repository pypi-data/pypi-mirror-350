import requests
from typing import Optional, Dict, Any

def post(endpoint: str, token: str, payload: Dict[str, Any], timeout: int = 30) -> requests.Response:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return requests.post(endpoint, json=payload, headers=headers, timeout=timeout)