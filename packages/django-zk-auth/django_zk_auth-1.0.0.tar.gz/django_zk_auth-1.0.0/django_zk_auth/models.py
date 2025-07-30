from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils import timezone
from typing import Optional, Dict, Any
import json
import uuid
import hashlib
from datetime import timedelta
from django.conf import settings
user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

# user = models.ForeignKey('django_zk_auth.ZKUser', on_delete=models.CASCADE)

class Session(models.Model):
    """Minimal session model to support foreign key reference."""
    created_at = models.DateTimeField(auto_now_add=True)

class ZKAuditLog(models.Model):
    """Audit log model for zero-knowledge auth events."""

    EVENT_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('verify', 'Verification'),
        # Add more types as needed
    ]

    event_type = models.CharField(max_length=32, choices=EVENT_TYPES)
    event_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    session = models.ForeignKey(Session, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField()
    previous_hash = models.CharField(max_length=64, null=True, blank=True)
    content_hash = models.CharField(max_length=64)

    class Meta:
        ordering = ['timestamp']

    def save(self, *args, **kwargs):
        from django_zk_auth.crypto.hash_utils import calculate_audit_hash
        self.content_hash = calculate_audit_hash(self)
        super().save(*args, **kwargs)


class ZKUserManager(BaseUserManager):
    """Custom user manager for ZK authentication"""
    
    def create_user(self, username: str, zk_commitment: str, **extra_fields) -> 'ZKUser':
        """Create and save a user with ZK commitment"""
        if not username:
            raise ValueError('Username is required')
        if not zk_commitment:
            raise ValueError('ZK commitment is required')
            
        username = self.normalize_email(username) if '@' in username else username
        user = self.model(username=username, zk_commitment=zk_commitment, **extra_fields)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username: str, zk_commitment: str, **extra_fields) -> 'ZKUser':
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
            
        return self.create_user(username, zk_commitment, **extra_fields)


class ZKUser(AbstractBaseUser, PermissionsMixin):
    """
    Zero-Knowledge User Model
    Stores only commitments, never actual secrets
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(blank=True, null=True)
    
    # ZK-specific fields
    zk_commitment = models.CharField(
        max_length=128,
        help_text="Poseidon hash commitment of user's secret",
        db_index=True
    )
    commitment_algorithm = models.CharField(
        max_length=32,
        default='poseidon',
        choices=[('poseidon', 'Poseidon Hash'), ('pedersen', 'Pedersen Commitment')]
    )
    proof_version = models.CharField(max_length=16, default='1.0')
    
    # Standard Django fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    
    # Security metadata
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(blank=True, null=True)
    
    objects = ZKUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['zk_commitment']
    
    class Meta:
        db_table = 'zk_auth_user'
        verbose_name = 'ZK User'
        verbose_name_plural = 'ZK Users'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['zk_commitment']),
            models.Index(fields=['is_active', 'date_joined']),
        ]
    
    def __str__(self) -> str:
        return f"ZKUser({self.username})"
    
    def clean(self):
        """Validate ZK commitment format"""
        super().clean()
        if self.zk_commitment:
            try:
                # Validate commitment is valid hex and correct length
                commitment_bytes = bytes.fromhex(self.zk_commitment)
                if len(commitment_bytes) != 32:  # 256-bit commitment
                    raise ValidationError('ZK commitment must be 256 bits (64 hex chars)')
            except ValueError:
                raise ValidationError('ZK commitment must be valid hexadecimal')
    
    def is_account_locked(self) -> bool:
        """Check if account is currently locked"""
        if self.account_locked_until:
            return timezone.now() < self.account_locked_until
        return False
    
    def lock_account(self, duration_minutes: int = 30):
        """Lock account for specified duration"""
        self.account_locked_until = timezone.now() + timedelta(minutes=duration_minutes)
        self.save(update_fields=['account_locked_until'])
    
    def unlock_account(self):
        """Unlock account and reset failed attempts"""
        self.account_locked_until = None
        self.failed_login_attempts = 0
        self.save(update_fields=['account_locked_until', 'failed_login_attempts'])
    
    def increment_failed_login(self):
        """Increment failed login attempts and lock if threshold reached"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:  # Configurable threshold
            self.lock_account()
        self.save(update_fields=['failed_login_attempts'])


class ZKSession(models.Model):
    """
    Zero-Knowledge Session Management
    Tracks active sessions with ephemeral nonces
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='zk_sessions')
    
    # Session data
    session_key = models.CharField(max_length=128, unique=True, db_index=True)
    current_nonce = models.CharField(max_length=64, blank=True)
    nonce_expires_at = models.DateTimeField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    last_accessed = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    # Security tracking
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    device_fingerprint = models.CharField(max_length=128, blank=True)
    
    class Meta:
        db_table = 'zk_auth_session'
        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self) -> str:
        return f"ZKSession({self.user.username}, {self.session_key[:8]}...)"
    
    def is_expired(self) -> bool:
        """Check if session is expired"""
        return timezone.now() > self.expires_at
    
    def is_nonce_valid(self) -> bool:
        """Check if current nonce is still valid"""
        if not self.current_nonce or not self.nonce_expires_at:
            return False
        return timezone.now() < self.nonce_expires_at
    
    def generate_nonce(self) -> str:
        """Generate new ephemeral nonce for challenge-response"""
        import secrets
        self.current_nonce = secrets.token_hex(32)
        self.nonce_expires_at = timezone.now() + timedelta(minutes=5)  # 5-minute nonce validity
        self.save(update_fields=['current_nonce', 'nonce_expires_at'])
        return self.current_nonce
    
    def invalidate(self):
        """Invalidate session"""
        self.is_active = False
        self.current_nonce = ''
        self.nonce_expires_at = None
        self.save(update_fields=['is_active', 'current_nonce', 'nonce_expires_at'])


class ZKProofLog(models.Model):
    """
    Audit Log for ZK Proof Verification
    NSA-grade logging for security analysis
    """
    
    VERIFICATION_CHOICES = [
        ('success', 'Verification Success'),
        ('failure', 'Verification Failure'),
        ('invalid_proof', 'Invalid Proof Structure'),
        ('expired_nonce', 'Expired Nonce'),
        ('replay_attack', 'Potential Replay Attack'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proof_logs')
    session = models.ForeignKey(ZKSession, on_delete=models.CASCADE, blank=True, null=True)
    
    # Proof metadata (never store actual proof for privacy)
    proof_hash = models.CharField(max_length=64, help_text="SHA-256 of proof JSON")
    verification_result = models.CharField(max_length=20, choices=VERIFICATION_CHOICES)
    nonce_used = models.CharField(max_length=64)
    
    # Timing analysis
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    verification_time_ms = models.PositiveIntegerField(help_text="Verification time in milliseconds")
    
    # Security context
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    request_fingerprint = models.CharField(max_length=128, blank=True)
    
    # Anomaly detection fields
    is_anomalous = models.BooleanField(default=False)
    anomaly_score = models.FloatField(blank=True, null=True)
    anomaly_reason = models.TextField(blank=True)
    
    class Meta:
        db_table = 'zk_auth_proof_log'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['verification_result', 'timestamp']),
            models.Index(fields=['is_anomalous', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]
    
    def __str__(self) -> str:
        return f"ZKProofLog({self.user.username}, {self.verification_result}, {self.timestamp})"
    
    @classmethod
    def log_verification(cls, user: ZKUser, session: Optional[ZKSession], 
                        proof_data: Dict[str, Any], result: str, 
                        verification_time_ms: int, request_meta: Dict[str, Any]) -> 'ZKProofLog':
        """Create audit log entry for proof verification"""
        
        # Hash the proof for audit without storing sensitive data
        proof_json = json.dumps(proof_data, sort_keys=True)
        proof_hash = hashlib.sha256(proof_json.encode()).hexdigest()
        
        log_entry = cls.objects.create(
            user=user,
            session=session,
            proof_hash=proof_hash,
            verification_result=result,
            nonce_used=proof_data.get('nonce', ''),
            verification_time_ms=verification_time_ms,
            ip_address=request_meta.get('ip_address', ''),
            user_agent=request_meta.get('user_agent', ''),
            request_fingerprint=request_meta.get('fingerprint', '')
        )
        
        # Run anomaly detection
        log_entry.detect_anomalies()
        return log_entry
    
    def detect_anomalies(self):
        """Simple anomaly detection based on timing and frequency"""
        
        # Check for timing anomalies (unusually fast/slow verification)
        recent_logs = ZKProofLog.objects.filter(
            user=self.user,
            timestamp__gte=timezone.now() - timedelta(hours=1)
        ).exclude(id=self.id)
        
        if recent_logs.exists():
            avg_time = recent_logs.aggregate(avg_time=models.Avg('verification_time_ms'))['avg_time']
            if avg_time and abs(self.verification_time_ms - avg_time) > avg_time * 2:
                self.is_anomalous = True
                self.anomaly_reason = f"Unusual verification time: {self.verification_time_ms}ms vs avg {avg_time:.1f}ms"
        
        # Check for frequency anomalies (too many attempts)
        recent_count = recent_logs.count()
        if recent_count > 10:  # More than 10 attempts per hour
            self.is_anomalous = True
            self.anomaly_reason = f"High frequency: {recent_count} attempts in last hour"
        
        if self.is_anomalous:
            self.save(update_fields=['is_anomalous', 'anomaly_reason'])


class ZKConfiguration(models.Model):
    """
    System-wide ZK Authentication Configuration
    """
    
    PROOF_SYSTEMS = [
        ('groth16', 'Groth16 (Fast verification)'),
        ('plonk', 'PLONK (Universal setup)'),
        ('stark', 'STARK (Transparent, quantum-resistant)'),
    ]
    
    # Singleton pattern - only one configuration
    id = models.AutoField(primary_key=True)
    
    # Cryptographic settings
    proof_system = models.CharField(max_length=20, choices=PROOF_SYSTEMS, default='groth16')
    hash_algorithm = models.CharField(max_length=20, default='poseidon')
    field_prime = models.CharField(max_length=128, default='21888242871839275222246405745257275088548364400416034343698204186575808495617')
    
    # Security parameters
    max_failed_attempts = models.PositiveIntegerField(default=5)
    account_lockout_minutes = models.PositiveIntegerField(default=30)
    nonce_validity_minutes = models.PositiveIntegerField(default=5)
    session_timeout_hours = models.PositiveIntegerField(default=24)
    
    # Performance settings
    enable_proof_caching = models.BooleanField(default=True)
    max_concurrent_verifications = models.PositiveIntegerField(default=100)
    verification_timeout_seconds = models.PositiveIntegerField(default=30)
    
    # Audit settings
    enable_audit_logging = models.BooleanField(default=True)
    enable_anomaly_detection = models.BooleanField(default=True)
    log_retention_days = models.PositiveIntegerField(default=90)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'zk_auth_configuration'
        verbose_name = 'ZK Configuration'
        verbose_name_plural = 'ZK Configuration'
    
    def save(self, *args, **kwargs):
        # Ensure singleton
        if not self.pk and ZKConfiguration.objects.exists():
            raise ValidationError('Only one ZK configuration is allowed')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls) -> 'ZKConfiguration':
        """Get or create the singleton configuration"""
        config, created = cls.objects.get_or_create(defaults={})
        return config
    
    def __str__(self) -> str:
        return f"ZK Configuration ({self.proof_system}, {self.hash_algorithm})"