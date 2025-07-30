"""
Django ZK Auth Views
Zero-Knowledge Authentication API Endpoints
"""
import json
import time
import logging
import uuid
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from django.conf import settings
from typing import Dict, Any, Optional, Tuple
from datetime import timedelta
from .models import ZKUser, ZKSession, ZKProofLog, ZKConfiguration
from .crypto.zk_system import ZKSystem
from .crypto.types import ZKProof, Nonce
from .utils import get_client_ip, get_request_fingerprint, rate_limit_check
from .exceptions import (
    ZKVerificationError, 
    InvalidProofError, 
    ExpiredNonceError,
    AccountLockedException,
    RateLimitExceededException
)

logger = logging.getLogger(__name__)


class ZKAuthMixin:
    """Common functionality for ZK authentication views"""
    
    def get_request_metadata(self, request) -> Dict[str, Any]:
        """Extract security metadata from request"""
        return {
            'ip_address': get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'fingerprint': get_request_fingerprint(request),
            'timestamp': timezone.now().isoformat()
        }
    
    def parse_json_body(self, request) -> Dict[str, Any]:
        """Safely parse JSON request body"""
        try:
            return json.loads(request.body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.warning(f"Invalid JSON in request: {e}")
            raise ValueError("Invalid JSON data")
    
    def create_error_response(self, message: str, code: str = 'error', 
                            status: int = 400) -> JsonResponse:
        """Create standardized error response"""
        return JsonResponse({
            'success': False,
            'error': {
                'code': code,
                'message': message
            }
        }, status=status)
    
    def create_success_response(self, data: Dict[str, Any] = None, 
                              message: str = 'Success') -> JsonResponse:
        """Create standardized success response"""
        response_data = {
            'success': True,
            'message': message
        }
        if data:
            response_data.update(data)
        return JsonResponse(response_data)


@method_decorator(csrf_exempt, name='dispatch')
class ZKRegistrationView(View, ZKAuthMixin):
    """
    Handle Zero-Knowledge user registration
    Accepts ZK commitment, never stores actual passwords
    """
    
    def post(self, request) -> JsonResponse:
        """Register new user with ZK commitment"""
        try:
            # Rate limiting check
            client_ip = get_client_ip(request)
            if not rate_limit_check(client_ip, 'registration', max_attempts=3, window_minutes=60):
                raise RateLimitExceededException("Too many registration attempts")
            
            # Parse request data
            try:
                data = self.parse_json_body(request)
            except ValueError:
                return self.create_error_response("Invalid JSON data", 'invalid_json')
            
            # Validate required fields
            required_fields = ['username', 'zk_commitment', 'proof']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return self.create_error_response(
                    f"Missing required fields: {', '.join(missing_fields)}", 
                    'missing_fields'
                )
            
            username = data['username']
            zk_commitment = data['zk_commitment'] 
            registration_proof = data['proof']
            email = data.get('email')
            
            # Check if user already exists
            if ZKUser.objects.filter(username=username).exists():
                return self.create_error_response(
                    "Username already exists", 
                    'username_exists', 
                    409
                )
            
            # Initialize ZK system
            zk_system = ZKSystem()
            
            # Verify registration proof
            start_time = time.time()
            try:
                is_valid = zk_system.verify_registration_proof(
                    commitment=zk_commitment,
                    proof=registration_proof
                )
                verification_time_ms = int((time.time() - start_time) * 1000)
                
                if not is_valid:
                    logger.warning(f"Invalid registration proof for username: {username}")
                    return self.create_error_response(
                        "Invalid proof provided", 
                        'invalid_proof'
                    )
                
            except Exception as e:
                logger.error(f"Registration proof verification failed: {e}")
                return self.create_error_response(
                    "Proof verification failed", 
                    'verification_error'
                )
            
            # Create new user
            try:
                user = ZKUser.objects.create_user(
                    username=username,
                    zk_commitment=zk_commitment,
                    email=email
                )
                
                logger.info(f"New ZK user registered: {username}")
                
                return self.create_success_response({
                    'user_id': str(user.id),
                    'username': user.username,
                    'verification_time_ms': verification_time_ms
                }, "User registered successfully")
                
            except Exception as e:
                logger.error(f"User creation failed: {e}")
                return self.create_error_response(
                    "User creation failed", 
                    'creation_error', 
                    500
                )
        
        except RateLimitExceededException as e:
            return self.create_error_response(str(e), 'rate_limit', 429)
        except Exception as e:
            logger.error(f"Unexpected error in registration: {e}")
            return self.create_error_response(
                "Internal server error", 
                'server_error', 
                500
            )

@method_decorator(csrf_exempt, name='dispatch')
class ZKLogoutView(View, ZKAuthMixin):
    """Handle Zero-Knowledge logout"""
    
    def post(self, request) -> JsonResponse:
        """Logout user and invalidate session"""
        try:
            if not request.user.is_authenticated:
                return self.create_error_response("Not logged in", 'not_authenticated')
            
            username = request.user.username
            
            # Invalidate ZK sessions
            ZKSession.objects.filter(
                user=request.user,
                session_key=request.session.session_key
            ).update(
                is_active=False,
                current_nonce='',
                nonce_expires_at=None
            )
            
            # Django logout
            logout(request)
            
            logger.info(f"User logged out: {username}")
            
            return self.create_success_response(message="Logout successful")
        
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return self.create_error_response("Logout failed", 'logout_error', 500)


@method_decorator(csrf_exempt, name='dispatch')
class ZKStatusView(View, ZKAuthMixin):
    """Get current authentication status"""
    
    def get(self, request) -> JsonResponse:
        """Get user authentication status"""
        try:
            if request.user.is_authenticated and hasattr(request.user, 'zk_commitment'):
                user = request.user
                
                # Get active session info
                session_info = None
                try:
                    zk_session = ZKSession.objects.get(
                        user=user,
                        session_key=request.session.session_key,
                        is_active=True
                    )
                    session_info = {
                        'session_id': str(zk_session.id),
                        'created_at': zk_session.created_at.isoformat(),
                        'last_accessed': zk_session.last_accessed.isoformat(),
                        'expires_at': zk_session.expires_at.isoformat()
                    }
                except ZKSession.DoesNotExist:
                    pass
                
                return self.create_success_response({
                    'authenticated': True,
                    'user': {
                        'id': str(user.id),
                        'username': user.username,
                        'email': user.email,
                        'date_joined': user.date_joined.isoformat(),
                        'last_login': user.last_login.isoformat() if user.last_login else None
                    },
                    'session': session_info,
                    'zk_info': {
                        'commitment_algorithm': user.commitment_algorithm,
                        'proof_version': user.proof_version
                    }
                })
            else:
                return self.create_success_response({
                    'authenticated': False
                })
        
        except Exception as e:
            logger.error(f"Error getting auth status: {e}")
            return self.create_error_response("Status check failed", 'status_error', 500)


@method_decorator(csrf_exempt, name='dispatch')
class ZKUserProfileView(View, ZKAuthMixin):
    """Manage user profile (authenticated users only)"""
    
    def get(self, request) -> JsonResponse:
        """Get user profile"""
        if not request.user.is_authenticated:
            return self.create_error_response("Authentication required", 'auth_required', 401)
        
        try:
            user = request.user
            
            # Get recent login activity
            recent_logs = ZKProofLog.objects.filter(
                user=user,
                verification_result='success'
            ).order_by('-timestamp')[:10]
            
            login_history = []
            for log in recent_logs:
                login_history.append({
                    'timestamp': log.timestamp.isoformat(),
                    'ip_address': log.ip_address,
                    'verification_time_ms': log.verification_time_ms
                })
            
            return self.create_success_response({
                'user': {
                    'id': str(user.id),
                    'username': user.username,
                    'email': user.email,
                    'date_joined': user.date_joined.isoformat(),
                    'last_login': user.last_login.isoformat() if user.last_login else None,
                    'is_active': user.is_active
                },
                'zk_info': {
                    'commitment_algorithm': user.commitment_algorithm,
                    'proof_version': user.proof_version,
                    'failed_attempts': user.failed_login_attempts,
                    'account_locked': user.is_account_locked()
                },
                'login_history': login_history
            })
        
        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            return self.create_error_response("Profile fetch failed", 'profile_error', 500)
    
    def patch(self, request) -> JsonResponse:
        """Update user profile (limited fields)"""
        if not request.user.is_authenticated:
            return self.create_error_response("Authentication required", 'auth_required', 401)
        
        try:
            data = self.parse_json_body(request)
            user = request.user
            
            # Only allow updating email
            if 'email' in data:
                user.email = data['email']
                user.save(update_fields=['email'])
            
            return self.create_success_response(message="Profile updated successfully")
        
        except ValueError:
            return self.create_error_response("Invalid JSON data", 'invalid_json')
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            return self.create_error_response("Profile update failed", 'update_error', 500)


@method_decorator(csrf_exempt, name='dispatch')
class ZKSystemStatusView(View, ZKAuthMixin):
    """System health and configuration status"""
    
    def get(self, request) -> JsonResponse:
        """Get ZK system status"""
        try:
            config = ZKConfiguration.get_config()
            
            # System health checks
            active_sessions = ZKSession.objects.filter(
                is_active=True,
                expires_at__gt=timezone.now()
            ).count()
            
            recent_verifications = ZKProofLog.objects.filter(
                timestamp__gte=timezone.now() - timedelta(hours=1)
            ).count()
            
            success_rate = 0
            if recent_verifications > 0:
                successful = ZKProofLog.objects.filter(
                    timestamp__gte=timezone.now() - timedelta(hours=1),
                    verification_result='success'
                ).count()
                success_rate = (successful / recent_verifications) * 100
            
            return self.create_success_response({
                'system': {
                    'proof_system': config.proof_system,
                    'hash_algorithm': config.hash_algorithm,
                    'version': '1.0.0'
                },
                'health': {
                    'active_sessions': active_sessions,
                    'verifications_last_hour': recent_verifications,
                    'success_rate_percent': round(success_rate, 2),
                    'audit_logging_enabled': config.enable_audit_logging,
                    'anomaly_detection_enabled': config.enable_anomaly_detection
                },
                'limits': {
                    'max_failed_attempts': config.max_failed_attempts,
                    'lockout_minutes': config.account_lockout_minutes,
                    'nonce_validity_minutes': config.nonce_validity_minutes,
                    'session_timeout_hours': config.session_timeout_hours
                }
            })
        
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return self.create_error_response("System status unavailable", 'status_error', 500)


# Function-based views for simple operations
@csrf_exempt
@require_http_methods(["POST"])
def refresh_nonce(request) -> JsonResponse:
    """Refresh nonce for existing session"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        session_id = data.get('session_id')
        
        if not session_id:
            return JsonResponse({
                'success': False,
                'error': {'code': 'missing_session_id', 'message': 'Session ID required'}
            }, status=400)
        
        try:
            session = ZKSession.objects.get(id=session_id, is_active=True)
            
            if session.is_expired():
                return JsonResponse({
                    'success': False,
                    'error': {'code': 'session_expired', 'message': 'Session expired'}
                }, status=410)
            
            # Generate new nonce
            nonce = session.generate_nonce()
            
            return JsonResponse({
                'success': True,
                'nonce': nonce,
                'expires_at': session.nonce_expires_at.isoformat()
            })
        
        except ZKSession.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': {'code': 'invalid_session', 'message': 'Invalid session'}
            }, status=404)
    
    except Exception as e:
        logger.error(f"Error refreshing nonce: {e}")
        return JsonResponse({
            'success': False,
            'error': {'code': 'server_error', 'message': 'Server error'}
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def cleanup_expired_sessions(request) -> JsonResponse:
    """Admin endpoint to cleanup expired sessions"""
    try:
        # This would typically be called by a cron job or admin
        expired_count = ZKSession.objects.filter(
            expires_at__lt=timezone.now()
        ).update(is_active=False)
        
        # Also cleanup old proof logs based on retention policy
        config = ZKConfiguration.get_config()
        retention_date = timezone.now() - timedelta(days=config.log_retention_days)
        old_logs_count = ZKProofLog.objects.filter(
            timestamp__lt=retention_date
        ).delete()[0]
        
        return JsonResponse({
            'success': True,
            'cleaned_up': {
                'expired_sessions': expired_count,
                'old_logs': old_logs_count
            }
        })

    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        return JsonResponse({
            'success': False,
            'error': {'code': 'cleanup_error', 'message': 'Cleanup failed'}
        }, status=500)



@method_decorator(csrf_exempt, name='dispatch')
class ZKLoginChallengeView(View, ZKAuthMixin):
    """
    Step 1 of ZK login: Generate challenge nonce
    """
    
    def post(self, request) -> JsonResponse:
        """Generate login challenge for user"""
        try:
            # Parse request
            try:
                data = self.parse_json_body(request)
            except ValueError:
                return self.create_error_response("Invalid JSON data", 'invalid_json')
            
            username = data.get('username')
            if not username:
                return self.create_error_response("Username is required", 'missing_username')
            
            # Find user
            try:
                user = ZKUser.objects.get(username=username, is_active=True)
            except ZKUser.DoesNotExist:
                # Don't reveal if user exists or not for security
                return self.create_error_response("Authentication failed", 'auth_failed')
            
            # Check if account is locked
            if user.is_account_locked():
                return self.create_error_response(
                    "Account temporarily locked", 
                    'account_locked', 
                    423
                )
            
            # Rate limiting
            client_ip = get_client_ip(request)
            if not rate_limit_check(client_ip, f'login_challenge:{username}', max_attempts=10, window_minutes=15):
                raise RateLimitExceededException("Too many challenge requests")
            
            # Create or get session
            session_key = request.session.session_key or str(uuid.uuid4())
            if not request.session.session_key:
                request.session.create()
                session_key = request.session.session_key
            
            # Get or create ZK session
            zk_session, created = ZKSession.objects.get_or_create(
                user=user,
                session_key=session_key,
                defaults={
                    'expires_at': timezone.now() + timedelta(hours=24),
                    'ip_address': get_client_ip(request),
                    'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    'device_fingerprint': get_request_fingerprint(request)
                }
            )
            
            # Generate fresh nonce
            nonce = zk_session.generate_nonce()
            
            logger.info(f"Login challenge generated for user: {username}")
            
            return self.create_success_response({
                'nonce': nonce,
                'session_id': str(zk_session.id),
                'expires_at': zk_session.nonce_expires_at.isoformat(),
                'commitment': user.zk_commitment  # Client needs this for proof
            }, "Challenge generated")
        
        except RateLimitExceededException as e:
            return self.create_error_response(str(e), 'rate_limit', 429)
        except Exception as e:
            logger.error(f"Error generating login challenge: {e}")
            return self.create_error_response("Server error", 'server_error', 500)


@method_decorator(csrf_exempt, name='dispatch')
class ZKLoginVerifyView(View, ZKAuthMixin):
    """
    Step 2 of ZK login: Verify proof against challenge
    """
    
    def post(self, request) -> JsonResponse:
        """Verify ZK proof for login"""
        start_time = time.time()
        verification_result = 'failure'
        user = None
        session = None
        
        try:
            # Parse request
            try:
                data = self.parse_json_body(request)
            except ValueError:
                return self.create_error_response("Invalid JSON data", 'invalid_json')
            
            # Validate required fields
            required_fields = ['username', 'session_id', 'proof']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return self.create_error_response(
                    f"Missing fields: {', '.join(missing_fields)}", 
                    'missing_fields'
                )
            
            username = data['username']
            session_id = data['session_id']
            proof_data = data['proof']
            
            # Find user and session
            try:
                user = ZKUser.objects.get(username=username, is_active=True)
                session = ZKSession.objects.get(
                    id=session_id, 
                    user=user, 
                    is_active=True
                )
            except (ZKUser.DoesNotExist, ZKSession.DoesNotExist):
                return self.create_error_response("Invalid session", 'invalid_session')
            
            # Check account status
            if user.is_account_locked():
                verification_result = 'account_locked'
                return self.create_error_response("Account locked", 'account_locked', 423)
            
            # Check session validity
            if session.is_expired():
                verification_result = 'expired_session'
                return self.create_error_response("Session expired", 'expired_session')
            
            # Check nonce validity
            if not session.is_nonce_valid():
                verification_result = 'expired_nonce'
                return self.create_error_response("Challenge expired", 'expired_nonce')
            
            # Rate limiting
            client_ip = get_client_ip(request)
            if not rate_limit_check(client_ip, f'login_verify:{username}', max_attempts=5, window_minutes=15):
                raise RateLimitExceededException("Too many verification attempts")
            
            # Verify ZK proof
            zk_system = ZKSystem()
            
            try:
                is_valid = zk_system.verify_login_proof(
                    commitment=user.zk_commitment,
                    nonce=session.current_nonce,
                    proof=proof_data
                )
                
                verification_time_ms = int((time.time() - start_time) * 1000)
                
                if is_valid:
                    verification_result = 'success'
                    
                    # Successful login
                    login(request, user)
                    user.last_login = timezone.now()
                    user.failed_login_attempts = 0
                    user.save(update_fields=['last_login', 'failed_login_attempts'])
                    
                    # Update session
                    session.last_accessed = timezone.now()
                    session.current_nonce = ''  # Invalidate nonce after use
                    session.nonce_expires_at = None
                    session.save(update_fields=['last_accessed', 'current_nonce', 'nonce_expires_at'])
                    
                    logger.info(f"Successful ZK login for user: {username}")
                    
                    return self.create_success_response({
                        'user_id': str(user.id),
                        'username': user.username,
                        'session_key': session.session_key,
                        'verification_time_ms': verification_time_ms
                    }, "Login successful")
                
                else:
                    verification_result = 'invalid_proof'
                    # Failed login
                    user.increment_failed_login()
                    logger.warning(f"Invalid ZK proof for user: {username}")
                    
                    return self.create_error_response(
                        "Authentication failed", 
                        'auth_failed'
                    )
            
            except Exception as e:
                verification_result = 'verification_error'
                logger.error(f"ZK proof verification error: {e}")
                return self.create_error_response(
                    "Verification failed", 
                    'verification_error'
                )
        
        except RateLimitExceededException as e:
            verification_result = 'rate_limit'
            return self.create_error_response(str(e), 'rate_limit', 429)
        except Exception as e:
            logger.error(f"Error in login verification: {e}")
            return self.create_error_response("Server error", 'server_error', 500)
        
        finally:
            # Always log the verification attempt for audit
            if user and session:
                verification_time_ms = int((time.time() - start_time) * 1000)
                request_meta = self.get_request_metadata(request)
                
                ZKProofLog.log_verification(
                    user=user,
                    session=session,
                    proof_data=data.get('proof', {}),
                    result=verification_result,
                    verification_time_ms=verification_time_ms,
                    request_meta=request_meta
                )
