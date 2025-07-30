"""
Custom exceptions for Django ZK Auth
"""

class ZKAuthError(Exception):
    """Base exception for all ZK Auth-related errors."""
    pass


class ZKVerificationError(ZKAuthError):
    """Raised when a ZK proof fails verification."""
    def __init__(self, message="Zero-Knowledge proof verification failed"):
        super().__init__(message)


class ZKInitializationError(ZKAuthError):
    """Raised when the ZK system fails to initialize."""
    def __init__(self, message="Failed to initialize ZK system"):
        super().__init__(message)


class ZKConfigurationError(ZKAuthError):
    """Raised when invalid or missing configuration is detected."""
    def __init__(self, message="Invalid ZK Auth configuration"):
        super().__init__(message)


class InvalidProofError(ZKVerificationError):
    """Raised when a provided ZK proof is invalid."""
    def __init__(self, message="The provided ZK proof is invalid"):
        super().__init__(message)


class ExpiredNonceError(ZKVerificationError):
    """Raised when a nonce used in the ZK proof has expired."""
    def __init__(self, message="The nonce has expired"):
        super().__init__(message)


class AccountLockedException(ZKAuthError):
    """Raised when a user account is locked due to repeated failed attempts."""
    def __init__(self, message="This account is locked"):
        super().__init__(message)


class RateLimitExceededException(ZKAuthError):
    """Raised when a user exceeds the allowed number of requests in a time period."""
    def __init__(self, message="Rate limit exceeded"):
        super().__init__(message)
