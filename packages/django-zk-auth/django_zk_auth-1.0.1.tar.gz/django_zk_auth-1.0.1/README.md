# django-zk-auth

🔐 A Django authentication package using zero-knowledge proofs (ZKPs) for enhanced privacy and security.

## Features

- Authenticate users via Zero-Knowledge proofs instead of passwords  
- Secure and privacy-preserving login flows  
- Custom authentication backends compatible with Django's auth system  
- Support for passwordless user registration using cryptographic commitments  
- Enhanced admin backend with additional security checks  
- Easy integration and configuration with existing Django projects  

---

## Installation

```bash
pip install django-zk-auth
```
## Configuration of Authentication Backends

To integrate Zero-Knowledge proof-based authentication into your Django project, configure the custom authentication backends provided by `django-zk-auth`.

## Using `ZKUser` and Authentication Backends in Your Django Project

To integrate `django-zk-auth` seamlessly, you can configure your Django settings to use the provided `ZKUser` model and authentication backends directly.

Here is an example configuration snippet, inspired by the `tests/test_settings.py` file included with the package, which you can adapt for your project:

```python
# settings.py (or your test settings)

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django_zk_auth",  # Enables ZK authentication app
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # In-memory DB for testing or quick dev setup
    }
}

AUTH_USER_MODEL = "django_zk_auth.ZKUser"  # Use the ZKUser model from the package

AUTHENTICATION_BACKENDS = [
    "django_zk_auth.auth_backend.ZKAdminAuthenticationBackend",  # Admin login with ZK proof
    "django_zk_auth.auth_backend.ZKAuthenticationBackend",       # Standard ZK user login
    "django_zk_auth.auth_backend.ZKPasswordlessBackend",         # Passwordless/registration backend
    "django.contrib.auth.backends.ModelBackend",                 # Django's fallback backend (optional)
]

# Optional: Speed up tests by simplifying password hashing
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Additional recommended settings
USE_TZ = True
TIME_ZONE = "UTC"

```
This setup allows your project to authenticate users through Zero-Knowledge proofs instead of conventional password authentication, enabling secure and privacy-preserving login flows and Leverage Django’s built-in authentication fallback if needed.



### Explanation of Authentication Backends:

## Authentication Backends Overview

- **ZKAuthenticationBackend**  
  Implements authentication using Zero-Knowledge proofs submitted by users. It verifies proof validity, account status, and manages failed login attempts, fully integrating with Django's user model through the custom `ZKUser`.

- **ZKPasswordlessBackend**  
  A fallback backend designed primarily for user registration flows. It authenticates users based on cryptographic commitments and registration proofs without requiring passwords.

- **ZKAdminAuthenticationBackend (Optional)**  
  Extends `ZKAuthenticationBackend` with additional security layers for Django admin access, ensuring only active staff users with valid ZK proofs can log in.

This modular backend design preserves the zero-knowledge property, enhancing security and privacy beyond traditional password schemes.

## Usage in Your Django Application

1. **User Login Flow:**  
   Replace traditional password authentication forms with a mechanism that collects Zero-Knowledge proof data (`zk_proof`) and a challenge `nonce`. These values are then passed to Django’s `authenticate()` method, which invokes the custom backends.

2. **Django Authentication Integration:**  
   Your views, middleware, or REST framework authentication classes can call:

   ```python
   from django.contrib.auth import authenticate, login

   user = authenticate(request, username=username, zk_proof=zk_proof_data, nonce=nonce)
   if user is not None:
       login(request, user)
       # User is now authenticated via Zero-Knowledge proof
   else:
       # Handle authentication failure

## Running Tests

The package includes an example `tests/test_settings.py` which configures an in-memory database and minimal apps for testing the authentication backend in isolation.

```bash
pytest -s tests/test_zksystem.py
```
## Running Specific Tests by Class
```bash
pytest -k TestZKSystem -s tests/test_zk_system.py
```
  
