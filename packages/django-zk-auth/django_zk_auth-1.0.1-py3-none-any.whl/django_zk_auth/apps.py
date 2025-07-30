
# django_zk_auth/apps.py
from django.apps import AppConfig
from django.conf import settings
from typing import Optional
import logging
import traceback

logger = logging.getLogger(__name__)

class DjangoZkAuthConfig(AppConfig):
    """Django ZK Auth application configuration"""
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_zk_auth"
    verbose_name = "Django Zero-Knowledge Authentication"
    
    def ready(self) -> None:
        """Initialize ZK cryptographic system"""
        try:
            from .crypto.zk_system import ZKSystem
            
            # Initialize the ZK system with settings
            zk_settings = getattr(settings, 'ZK_AUTH_SETTINGS', {})
            ZKSystem.initialize(zk_settings)
            
            logger.info("Django ZK Auth system initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize ZK Auth system:\n%s", traceback.format_exc())
   

