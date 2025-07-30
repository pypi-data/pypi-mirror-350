"""
Django ZK Auth Backend
Custom authentication backend for Zero-Knowledge proof authentication
"""

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from typing import Optional, Any
import logging

from .models import ZKUser
from .crypto.zk_system import ZKSystem
from .exceptions import ZKVerificationError

logger = logging.getLogger(__name__)


class ZKAuthenticationBackend(BaseBackend):
    """
    Zero-Knowledge Proof Authentication Backend
    
    This backend handles authentication using ZK proofs instead of passwords.
    It integrates with Django's authentication system while maintaining
    zero-knowledge properties.
    """
    
    def authenticate(self, request, username: str = None, zk_proof: dict = None, 
                    nonce: str = None, **kwargs) -> Optional[ZKUser]:
        """
        Authenticate user using Zero-Knowledge proof
        
        Args:
            request: HTTP request object
            username: Username to authenticate
            zk_proof: Zero-knowledge proof data
            nonce: Challenge nonce from server
            **kwargs: Additional authentication parameters
            
        Returns:
            ZKUser instance if authentication successful, None otherwise
        """
        
        if not all([username, zk_proof, nonce]):
            logger.debug("ZK authentication missing required parameters")
            return None
        
        try:
            # Get user by username
            user = ZKUser.objects.get(username=username, is_active=True)
            
            # Check if account is locked
            if user.is_account_locked():
                logger.warning(f"Authentication attempted on locked account: {username}")
                return None
            
            # Initialize ZK system
            zk_system = ZKSystem()
            
            # Verify ZK proof
            is_valid = zk_system.verify_login_proof(
                commitment=user.zk_commitment,
                nonce=nonce,
                proof=zk_proof
            )
            
            if is_valid:
                logger.info(f"Successful ZK authentication for user: {username}")
                
                # Reset failed login attempts on successful auth
                if user.failed_login_attempts > 0:
                    user.failed_login_attempts = 0
                    user.save(update_fields=['failed_login_attempts'])
                
                return user
            else:
                logger.warning(f"Invalid ZK proof for user: {username}")
                
                # Increment failed attempts
                user.increment_failed_login()
                return None
        
        except ZKUser.DoesNotExist:
            logger.warning(f"ZK authentication attempted for non-existent user: {username}")
            return None
        
        except ZKVerificationError as e:
            logger.error(f"ZK verification error for user {username}: {e}")
            return None
        
        except Exception as e:
            logger.error(f"Unexpected error in ZK authentication for {username}: {e}")
            return None
    
    def get_user(self, user_id: Any) -> Optional[ZKUser]:
        """
        Get user by ID
        
        Args:
            user_id: User identifier
            
        Returns:
            ZKUser instance if found, None otherwise
        """
        try:
            return ZKUser.objects.get(pk=user_id, is_active=True)
        except ZKUser.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {e}")
            return None
    
    def user_can_authenticate(self, user: ZKUser) -> bool:
        """
        Check if user can authenticate
        
        Args:
            user: ZKUser instance
            
        Returns:
            True if user can authenticate, False otherwise
        """
        if not isinstance(user, ZKUser):
            return False
        
        return (
            user.is_active and 
            not user.is_account_locked() and
            user.zk_commitment  # Must have valid commitment
        )
    
    def has_perm(self, user_obj: ZKUser, perm: str, obj: Any = None) -> bool:
        """
        Check if user has specific permission
        
        Args:
            user_obj: ZKUser instance
            perm: Permission string
            obj: Object to check permission for
            
        Returns:
            True if user has permission, False otherwise
        """
        if not isinstance(user_obj, ZKUser) or not user_obj.is_active:
            return False
        
        # Delegate to Django's default permission checking
        return user_obj.has_perm(perm, obj)
    
    def has_module_perms(self, user_obj: ZKUser, app_label: str) -> bool:
        """
        Check if user has permissions for app module
        
        Args:
            user_obj: ZKUser instance
            app_label: Django app label
            
        Returns:
            True if user has module permissions, False otherwise
        """
        if not isinstance(user_obj, ZKUser) or not user_obj.is_active:
            return False
        
        # Delegate to Django's default permission checking
        return user_obj.has_module_perms(app_label)


class ZKAdminAuthenticationBackend(ZKAuthenticationBackend):
    """
    Extended ZK Authentication Backend for Django Admin
    
    Provides additional security checks for admin access
    """
    
    def authenticate(self, request, username: str = None, zk_proof: dict = None, 
                    nonce: str = None, **kwargs) -> Optional[ZKUser]:
        """
        Authenticate admin user with additional security checks
        """
        user = super().authenticate(request, username, zk_proof, nonce, **kwargs)
        
        if user and self.user_can_authenticate_admin(user):
            return user
        
        return None
    
    def user_can_authenticate_admin(self, user: ZKUser) -> bool:
        """
        Check if user can authenticate for admin access
        
        Args:
            user: ZKUser instance
            
        Returns:
            True if user can access admin, False otherwise
        """
        return (
            self.user_can_authenticate(user) and
            user.is_staff and
            user.is_active
        )
    
    def has_perm(self, user_obj: ZKUser, perm: str, obj: Any = None) -> bool:
        """
        Enhanced permission checking for admin users
        """
        if not self.user_can_authenticate_admin(user_obj):
            return False
        
        return super().has_perm(user_obj, perm, obj)


class ZKPasswordlessBackend(BaseBackend):
    """
    Fallback backend for passwordless operations
    
    This backend allows certain operations without traditional password
    authentication, but still requires ZK proof validation for security.
    """
    
    def authenticate(self, request, commitment: str = None, 
                    registration_proof: dict = None, **kwargs) -> Optional[ZKUser]:
        """
        Authenticate using commitment and registration proof
        
        Used primarily for user registration flow
        
        Args:
            request: HTTP request object
            commitment: ZK commitment hash
            registration_proof: Proof of knowledge of commitment
            **kwargs: Additional parameters
            
        Returns:
            Temporary user object for registration, None if invalid
        """
        if not all([commitment, registration_proof]):
            return None
        
        try:
            # Initialize ZK system
            zk_system = ZKSystem()
            
            # Verify registration proof
            is_valid = zk_system.verify_registration_proof(
                commitment=commitment,
                proof=registration_proof
            )
            
            if is_valid:
                # Create temporary user object (not saved to DB)
                # This is used during registration flow
                temp_user = ZKUser(
                    username='temp_registration_user',
                    zk_commitment=commitment,
                    is_active=False  # Not active until properly registered
                )
                return temp_user
            
            return None
        
        except Exception as e:
            logger.error(f"Error in passwordless authentication: {e}")
            return None
    
    def get_user(self, user_id: Any) -> Optional[ZKUser]:
        """Get user by ID"""
        try:
            return ZKUser.objects.get(pk=user_id)
        except ZKUser.DoesNotExist:
            return None


# Utility functions for backend configuration

def get_zk_backends() -> list:
    """
    Get list of ZK authentication backends
    
    Returns:
        List of backend class paths
    """
    return [
        'django_zk_auth.auth_backend.ZKAuthenticationBackend',
        'django_zk_auth.auth_backend.ZKPasswordlessBackend',
    ]

def get_zk_admin_backends() -> list:
    """
    Get list of ZK authentication backends for admin
    
    Returns:
        List of backend class paths including admin backend
    """
    return [
        'django_zk_auth.auth_backend.ZKAdminAuthenticationBackend',
        'django_zk_auth.auth_backend.ZKAuthenticationBackend',
        'django_zk_auth.auth_backend.ZKPasswordlessBackend',
    ]