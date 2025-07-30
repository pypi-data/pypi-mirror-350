from django.urls import path
from .views import (
    ZKRegistrationView,
    ZKLogoutView,
    ZKStatusView,
    ZKUserProfileView,
    ZKSystemStatusView,
    ZKLoginChallengeView,
    ZKLoginVerifyView,
    refresh_nonce,
    cleanup_expired_sessions
)

urlpatterns = [
    path('register/', ZKRegistrationView.as_view(), name='zk_register'),
    path('logout/', ZKLogoutView.as_view(), name='zk_logout'),
    path('status/', ZKStatusView.as_view(), name='zk_status'),
    path('profile/', ZKUserProfileView.as_view(), name='zk_profile'),
    path('system/status/', ZKSystemStatusView.as_view(), name='zk_system_status'),
    path('login/challenge/', ZKLoginChallengeView.as_view(), name='zk_login_challenge'),
    path('login/verify/', ZKLoginVerifyView.as_view(), name='zk_login_verify'),
    path('refresh-nonce/', refresh_nonce, name='refresh_nonce'),
    path('cleanup/', cleanup_expired_sessions, name='cleanup_expired_sessions'),
]