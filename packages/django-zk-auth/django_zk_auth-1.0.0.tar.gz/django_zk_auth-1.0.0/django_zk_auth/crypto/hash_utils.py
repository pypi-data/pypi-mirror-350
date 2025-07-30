"""Utility functions for cryptographic hashing, client info extraction, and audit chain integrity."""

import hashlib
import secrets
import hmac
from typing import Union, Dict, Any, List, TYPE_CHECKING
from django.utils import timezone

if TYPE_CHECKING:
    from ..models import ZKAuditLog


def secure_random(length: int = 32) -> str:
    """
    Generate a cryptographically secure random hexadecimal string.

    Args:
        length (int): Number of bytes. Default is 32.

    Returns:
        str: Hexadecimal string of length 2 * `length`.
    """
    return secrets.token_hex(length)


def calculate_audit_hash(audit_log: 'ZKAuditLog') -> str:
    """
    Calculate a deterministic hash of the audit log's content.

    Args:
        audit_log (ZKAuditLog): The audit log entry.

    Returns:
        str: SHA-256 hash of the structured log content.
    """
    content = {
        'event_type': audit_log.event_type,
        'event_data': audit_log.event_data,
        'timestamp': audit_log.timestamp.isoformat(),
        'user_id': str(audit_log.user.id) if audit_log.user else None,
        'session_id': str(audit_log.session.id) if audit_log.session else None,
        'ip_address': audit_log.ip_address,
        'previous_hash': audit_log.previous_hash,
    }
    content_str = str(sorted(content.items()))
    return hashlib.sha256(content_str.encode('utf-8')).hexdigest()


def verify_audit_chain(audit_logs: List['ZKAuditLog']) -> bool:
    """
    Verify the integrity of an ordered list of audit logs.

    Args:
        audit_logs (List[ZKAuditLog]): List of audit log entries.

    Returns:
        bool: True if all logs have valid hashes and are correctly chained, else False.
    """
    if not audit_logs:
        return True

    sorted_logs = sorted(audit_logs, key=lambda log: log.timestamp)

    for i, log in enumerate(sorted_logs):
        if log.content_hash != calculate_audit_hash(log):
            return False
        if i > 0 and log.previous_hash != sorted_logs[i - 1].content_hash:
            return False

    return True


def constant_time_compare(a: Union[str, bytes], b: Union[str, bytes]) -> bool:
    """
    Compare two values in constant time to prevent timing attacks.

    Args:
        a (str | bytes): First value.
        b (str | bytes): Second value.

    Returns:
        bool: True if values are equal, else False.
    """
    if isinstance(a, str):
        a = a.encode('utf-8')
    if isinstance(b, str):
        b = b.encode('utf-8')
    return hmac.compare_digest(a, b)


def rate_limit_key(user_id: str, action: str, window_start: int) -> str:
    """
    Construct a Redis-style key for rate limiting.

    Args:
        user_id (str): Unique user identifier.
        action (str): Action name.
        window_start (int): Timestamp for rate limiting window.

    Returns:
        str: Redis-style key.
    """
    return f"zk_auth:rate_limit:{user_id}:{action}:{window_start}"


def extract_client_info(request) -> Dict[str, Any]:
    """
    Extract basic client metadata from a Django request object.

    Args:
        request: Django request object.

    Returns:
        Dict[str, Any]: Dictionary with IP address, user agent, etc.
    """
    return {
        'ip_address': get_client_ip(request),
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'accept_language': request.META.get('HTTP_ACCEPT_LANGUAGE', ''),
        'referer': request.META.get('HTTP_REFERER', ''),
    }


def get_client_ip(request) -> str:
    """
    Safely extract client IP address from request headers.

    Args:
        request: Django request object.

    Returns:
        str: Best-effort client IP.
    """
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()

    real_ip = request.META.get('HTTP_X_REAL_IP')
    if real_ip:
        return real_ip.strip()

    return request.META.get('REMOTE_ADDR', '127.0.0.1')
