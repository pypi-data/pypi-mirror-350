import datetime
import hashlib
import hmac
from typing import Any

from fastlink.exceptions import ExpirationError, HashMismatchError


def compute_hmac_sha256(payload: dict[str, Any], secret_key: str) -> str:
    data_check_string = "\n".join(sorted(f"{k}={v}" for k, v in payload.items()))
    return hmac.new(
        hashlib.sha256(secret_key.encode()).digest(),
        data_check_string.encode(),
        "sha256",
    ).hexdigest()


def verify_hmac_sha256(payload: dict[str, Any], expected_hash: str, secret_key: str) -> None:
    computed_hash = compute_hmac_sha256(payload, secret_key)
    if not hmac.compare_digest(computed_hash, expected_hash):
        raise HashMismatchError


def check_expiration(payload: dict[str, Any], expires_in: int = 300) -> None:
    dt = datetime.datetime.fromtimestamp(payload["auth_date"], tz=datetime.UTC)
    now = datetime.datetime.now(tz=datetime.UTC)
    if now - dt > datetime.timedelta(seconds=expires_in):
        raise ExpirationError
