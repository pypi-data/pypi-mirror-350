from django.contrib import admin
from .models import ZKUser, ZKSession, ZKProofLog, ZKAuditLog, ZKConfiguration, Session

@admin.register(ZKUser)
class ZKUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'zk_commitment']
    list_filter = ['is_active', 'is_staff']

@admin.register(ZKSession)
class ZKSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'is_active', 'created_at']
    search_fields = ['session_key']

@admin.register(ZKProofLog)
class ZKProofLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'verification_result', 'timestamp', 'is_anomalous']
    search_fields = ['proof_hash', 'nonce_used']

@admin.register(ZKAuditLog)
class ZKAuditLogAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'timestamp', 'ip_address', 'user']
    search_fields = ['ip_address']

@admin.register(ZKConfiguration)
class ZKConfigurationAdmin(admin.ModelAdmin):
    list_display = ['proof_system', 'hash_algorithm', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

admin.site.register(Session)
