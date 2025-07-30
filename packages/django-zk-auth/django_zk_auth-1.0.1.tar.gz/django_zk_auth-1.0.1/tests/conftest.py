# tests/conftest.py
import sys
from pathlib import Path
import os
import django
from django.conf import settings

from collections import Counter
import pytest


# Add the parent directory of django_zk_auth to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
@pytest.fixture(scope='session', autouse=True)
def django_setup():
    django.setup()

if not settings.configured:
    os.environ['DJANGO_SETTINGS_MODULE'] = "tests.test_settings"
    django.setup()

counts = Counter(settings.INSTALLED_APPS)
duplicates = [app for app, count in counts.items() if count > 1]
print("Duplicate apps in INSTALLED_APPS:", duplicates)

