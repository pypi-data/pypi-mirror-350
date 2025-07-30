import re
import requests
from typing import Dict, Any
from datetime import datetime, date

# regex for a very basic email validation
_EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


class PayloadValidationError(ValueError):
    """Raised when the payload is missing required fields or has invalid values."""


def _validate_payload(payload: Dict[str, Any]) -> None:
    # Top‐level required fields
    required = {
        "user_id": str,
        "email_address": str,
        "user_name": str,
        "repo_object": dict,
    }
    for field, typ in required.items():
        if field not in payload:
            raise PayloadValidationError(f"Missing required field: '{field}'")
        if not isinstance(payload[field], typ):
            raise PayloadValidationError(f"Field '{field}' must be of type {typ.__name__}")

    # email format
    if not _EMAIL_RE.match(payload["email_address"]):
        raise PayloadValidationError("Invalid email address format")

    # repo_object sub‐fields
    repo = payload["repo_object"]
    repo_required = {
        "repo_name": str,
        "repo_source": str,
        "repo_url": str,
        "repo_branch": str,
    }
    for rfield, rtyp in repo_required.items():
        if rfield not in repo:
            raise PayloadValidationError(f"Missing repo_object.{rfield}")
        if not isinstance(repo[rfield], rtyp):
            raise PayloadValidationError(f"repo_object.{rfield} must be a {rtyp.__name__}")

    # you can add more checks here (URL validation, branch name patterns, etc.)


def _populate_metadata(payload: Dict[str, Any]) -> None:
    """Autofill metadata.created_by/on and updated_by/on."""
    user = payload["user_id"]
    today = date.today().isoformat()
    payload["metadata"] = {
        "created_by": user,
        "created_on": today,
        "updated_by": user,
        "updated_on": today,
    }


def post(
    endpoint: str,
    token: str,
    payload: Dict[str, Any],
    timeout: int = 30
) -> requests.Response:
    """
    Send a POST with validated payload and auto‐populated metadata.

    Raises:
        PayloadValidationError: if payload is missing required data.
        requests.RequestException: on network failures.
    """
    # 1) Validate schema
    _validate_payload(payload)

    # 2) Add metadata
    _populate_metadata(payload)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return requests.post(endpoint, json={"body": payload}, headers=headers, timeout=timeout)
