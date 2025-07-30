import pytest
from unittest.mock import MagicMock
from django.utils import timezone
from django_zk_auth.crypto import hash_utils
import sys
import os
import logging


# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_secure_random_length():
    token = hash_utils.secure_random(16)
    assert isinstance(token, str)
    assert len(token) == 32  # 16 bytes = 32 hex characters


def test_constant_time_compare_equal():
    assert hash_utils.constant_time_compare("abc123", "abc123") is True


def test_constant_time_compare_unequal():
    assert hash_utils.constant_time_compare("abc123", "xyz789") is False


def test_rate_limit_key_format():
    key = hash_utils.rate_limit_key("user123", "login", 1680000000)
    assert key == "zk_auth:rate_limit:user123:login:1680000000"


def test_get_client_ip_from_x_forwarded_for():
    request = MagicMock()
    request.META = {"HTTP_X_FORWARDED_FOR": "1.2.3.4, 5.6.7.8"}
    assert hash_utils.get_client_ip(request) == "1.2.3.4"


def test_get_client_ip_from_real_ip():
    request = MagicMock()
    request.META = {"HTTP_X_REAL_IP": "9.8.7.6"}
    assert hash_utils.get_client_ip(request) == "9.8.7.6"


def test_get_client_ip_from_remote_addr():
    request = MagicMock()
    request.META = {"REMOTE_ADDR": "10.0.0.1"}
    assert hash_utils.get_client_ip(request) == "10.0.0.1"


def test_get_client_ip_fallback():
    request = MagicMock()
    request.META = {}
    assert hash_utils.get_client_ip(request) == "127.0.0.1"


def test_extract_client_info():
    request = MagicMock()
    request.META = {
        "HTTP_USER_AGENT": "TestAgent",
        "HTTP_ACCEPT_LANGUAGE": "en-US",
        "HTTP_REFERER": "https://example.com",
        "HTTP_X_FORWARDED_FOR": "1.2.3.4",
    }
    info = hash_utils.extract_client_info(request)
    assert info["ip_address"] == "1.2.3.4"
    assert info["user_agent"] == "TestAgent"
    assert info["accept_language"] == "en-US"
    assert info["referer"] == "https://example.com"


# Dummy model for audit log
class DummyUser:
    def __init__(self, id): self.id = id

class DummySession:
    def __init__(self, id): self.id = id

class DummyAuditLog:
    def __init__(self, event_type, event_data, timestamp, user, session, ip_address, previous_hash):
        self.event_type = event_type
        self.event_data = event_data
        self.timestamp = timestamp
        self.user = user
        self.session = session
        self.ip_address = ip_address
        self.previous_hash = previous_hash
        self.content_hash = hash_utils.calculate_audit_hash(self)


def test_calculate_audit_hash_determinism():
    timestamp = timezone.now()
    user = DummyUser("u1")
    session = DummySession("s1")
    log1 = DummyAuditLog("login", {"foo": "bar"}, timestamp, user, session, "1.2.3.4", "prevhash")
    log2 = DummyAuditLog("login", {"foo": "bar"}, timestamp, user, session, "1.2.3.4", "prevhash")
    assert log1.content_hash == log2.content_hash


def test_verify_audit_chain_success():
    timestamp = timezone.now()
    user = DummyUser("u1")
    session = DummySession("s1")
    log1 = DummyAuditLog("event1", {"a": 1}, timestamp, user, session, "1.1.1.1", None)
    log2 = DummyAuditLog("event2", {"b": 2}, timestamp, user, session, "1.1.1.1", log1.content_hash)
    assert hash_utils.verify_audit_chain([log1, log2]) is True


def test_verify_audit_chain_failure_on_content_hash():
    timestamp = timezone.now()
    user = DummyUser("u1")
    session = DummySession("s1")
    log1 = DummyAuditLog("event1", {"a": 1}, timestamp, user, session, "1.1.1.1", None)
    log1.content_hash = "tampered"
    assert hash_utils.verify_audit_chain([log1]) is False


def test_verify_audit_chain_failure_on_linkage():
    timestamp = timezone.now()
    user = DummyUser("u1")
    session = DummySession("s1")
    log1 = DummyAuditLog("event1", {"a": 1}, timestamp, user, session, "1.1.1.1", None)
    log2 = DummyAuditLog("event2", {"b": 2}, timestamp, user, session, "1.1.1.1", "wronghash")
    assert hash_utils.verify_audit_chain([log1, log2]) is False


def test_verify_audit_chain_empty():
    assert hash_utils.verify_audit_chain([]) is True
