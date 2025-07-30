"""
Django ZK Auth Utilities
Helper functions for Zero-Knowledge authentication
"""

from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from typing import Dict, Any, Optional, Tuple
import hashlib
import ipaddress
import json
import time
import secrets
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


def get_client_ip(request) -> str:
    """
    Extract client IP address from request
    
    Args:
        request: Django HTTP request object
        
    Returns:
        Client IP address as string
    """
    # Try X-Forwarded-For header first (for proxy/load balancer setups)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Take the first IP in the chain
        ip = x_forwarded_for.split(',')[0].strip()
        try:
            # Validate IP address
            ipaddress.ip_address(ip)
            return ip
        except ValueError:
            pass
    
    # Try X-Real-IP header (common with nginx)
    x_real_ip = request.META.get('HTTP_X_REAL_IP')
    if x_real_ip:
        try:
            ipaddress.ip_address(x_real_ip)
            return x_real_ip
        except ValueError:
            pass
    
    # Fall back to REMOTE_ADDR
    remote_addr = request.META.get('REMOTE_ADDR', '127.0.0.1')
    try:
        ipaddress.ip_address(remote_addr)
        return remote_addr
    except ValueError:
        return '127.0.0.1'


def get_request_fingerprint(request) -> str:
    """
    Generate fingerprint for request based on headers and metadata
    
    Args:
        request: Django HTTP request object
        
    Returns:
        SHA-256 hash of request fingerprint
    """
    fingerprint_data = {
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'accept_language': request.META.get('HTTP_ACCEPT_LANGUAGE', ''),
        'accept_encoding': request.META.get('HTTP_ACCEPT_ENCODING', ''),
        'accept': request.META.get('HTTP_ACCEPT', ''),
        'connection': request.META.get('HTTP_CONNECTION', ''),
        'dnt': request.META.get('HTTP_DNT', ''),
        'cache_control': request.META.get('HTTP_CACHE_CONTROL', ''),
    }
    
    # Create deterministic fingerprint
    fingerprint_json = json.dumps(fingerprint_data, sort_keys=True)
    return hashlib.sha256(fingerprint_json.encode()).hexdigest()


def rate_limit_check(identifier: str, action: str, max_attempts: int = 5, 
                    window_minutes: int = 15) -> bool:
    """
    Check if action is rate limited for given identifier
    
    Args:
        identifier: Unique identifier (IP, username, etc.)
        action: Action being rate limited
        max_attempts: Maximum attempts allowed in window
        window_minutes: Time window in minutes
        
    Returns:
        True if action is allowed, False if rate limited
    """
    cache_key = f"zk_rate_limit:{action}:{identifier}"
    
    try:
        # Get current attempt count
        current_data = cache.get(cache_key, {'count': 0, 'first_attempt': time.time()})
        
        now = time.time()
        window_seconds = window_minutes * 60
        
        # Check if window has expired
        if now - current_data['first_attempt'] > window_seconds:
            # Reset counter
            current_data = {'count': 1, 'first_attempt': now}
        else:
            # Increment counter
            current_data['count'] += 1
        
        # Store updated data
        cache.set(cache_key, current_data, timeout=window_seconds)
        
        # Check if limit exceeded
        if current_data['count'] > max_attempts:
            logger.warning(f"Rate limit exceeded for {identifier}:{action} - {current_data['count']} attempts")
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"Rate limit check error: {e}")
        # Fail open - allow the action if cache fails
        return True


def generate_secure_nonce(length: int = 32) -> str:
    """
    Generate cryptographically secure nonce
    
    Args:
        length: Length of nonce in bytes
        
    Returns:
        Hex-encoded nonce string
    """
    return secrets.token_hex(length)


def hash_proof_data(proof_data: Dict[str, Any]) -> str:
    """
    Create deterministic hash of proof data for audit logging
    
    Args:
        proof_data: ZK proof data dictionary
        
    Returns:
        SHA-256 hash of proof data
    """
    # Remove sensitive fields and create deterministic JSON
    sanitized_data = {k: v for k, v in proof_data.items() 
                     if k not in ['private_inputs', 'witness']}
    
    proof_json = json.dumps(sanitized_data, sort_keys=True)
    return hashlib.sha256(proof_json.encode()).hexdigest()


def validate_commitment_format(commitment: str) -> bool:
    """
    Validate ZK commitment format
    
    Args:
        commitment: Commitment string to validate
        
    Returns:
        True if valid format, False otherwise
    """
    try:
        # Should be hex string of correct length (64 chars = 32 bytes = 256 bits)
        if len(commitment) != 64:
            return False
        
        # Should be valid hex
        bytes.fromhex(commitment)
        return True
    
    except ValueError:
        return False


def timing_safe_compare(a: str, b: str) -> bool:
    """
    Timing-safe string comparison to prevent timing attacks
    
    Args:
        a: First string
        b: Second string
        
    Returns:
        True if strings are equal, False otherwise
    """
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    
    return result == 0


def cleanup_expired_cache_entries(prefix: str = "zk_rate_limit") -> int:
    """
    Clean up expired cache entries with given prefix
    
    Args:
        prefix: Cache key prefix to clean
        
    Returns:
        Number of entries cleaned up
    """
    try:
        # This is cache-backend specific
        # For Redis: could iterate through keys
        # For Memcached: keys expire automatically
        # For database cache: could run cleanup query
        
        # Placeholder implementation
        logger.info(f"Cache cleanup requested for prefix: {prefix}")
        return 0
    
    except Exception as e:
        logger.error(f"Cache cleanup error: {e}")
        return 0


def get_system_health_metrics() -> Dict[str, Any]:
    """
    Get system health metrics for monitoring
    
    Returns:
        Dictionary of health metrics
    """
    from .models import ZKUser, ZKSession, ZKProofLog
    
    try:
        now = timezone.now()
        one_hour_ago = now - timedelta(hours=1)
        one_day_ago = now - timedelta(days=1)
        
        metrics = {
            'timestamp': now.isoformat(),
            'users': {
                'total_active': ZKUser.objects.filter(is_active=True).count(),
                'total_locked': ZKUser.objects.filter(
                    account_locked_until__gt=now
                ).count(),
                'new_today': ZKUser.objects.filter(
                    date_joined__gte=one_day_ago
                ).count()
            },
            'sessions': {
                'active': ZKSession.objects.filter(
                    is_active=True,
                    expires_at__gt=now
                ).count(),
                'expired_cleanup_needed': ZKSession.objects.filter(
                    expires_at__lt=now,
                    is_active=True
                ).count()
            },
            'authentication': {
                'verifications_last_hour': ZKProofLog.objects.filter(
                    timestamp__gte=one_hour_ago
                ).count(),
                'successful_last_hour': ZKProofLog.objects.filter(
                    timestamp__gte=one_hour_ago,
                    verification_result='success'
                ).count(),
                'failed_last_hour': ZKProofLog.objects.filter(
                    timestamp__gte=one_hour_ago,
                    verification_result='failure'
                ).count(),
                'anomalies_last_hour': ZKProofLog.objects.filter(
                    timestamp__gte=one_hour_ago,
                    is_anomalous=True
                ).count()
            }
        }
        
        # Calculate success rate
        total_verifications = metrics['authentication']['verifications_last_hour']
        if total_verifications > 0:
            success_rate = (metrics['authentication']['successful_last_hour'] / 
                          total_verifications) * 100
            metrics['authentication']['success_rate_percent'] = round(success_rate, 2)
        else:
            metrics['authentication']['success_rate_percent'] = 0.0
        
        return metrics
    
    except Exception as e:
        logger.error(f"Error getting health metrics: {e}")
        return {
            'timestamp': timezone.now().isoformat(),
            'error': str(e)
        }


def export_auth_logs(
    since: Optional[timezone.datetime] = None,
    limit: int = 1000
) -> Tuple[bool, Optional[str]]:
    """
    Export recent authentication proof logs to JSON file for external analysis or audit.

    Args:
        since: Optional datetime to filter logs from
        limit: Maximum number of logs to export

    Returns:
        Tuple with success flag and filepath or error message
    """
    from .models import ZKProofLog
    import os
    from django.core.serializers import serialize

    try:
        now = timezone.now()
        if since is None:
            since = now - timedelta(days=1)

        logs = ZKProofLog.objects.filter(timestamp__gte=since).order_by('-timestamp')[:limit]

        data = serialize('json', logs)

        # Save to file (you can adjust this path as needed)
        export_dir = getattr(settings, 'ZK_EXPORT_DIR', '/tmp')
        os.makedirs(export_dir, exist_ok=True)
        file_path = os.path.join(export_dir, f"zk_auth_logs_{now.strftime('%Y%m%d%H%M%S')}.json")

        with open(file_path, 'w') as f:
            f.write(data)

        logger.info(f"Exported {len(logs)} ZK auth logs to {file_path}")
        return True, file_path

    except Exception as e:
        logger.error(f"Error exporting auth logs: {e}")
        return False, str(e)