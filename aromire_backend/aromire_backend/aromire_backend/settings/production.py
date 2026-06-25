from .base import *

import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv


# =============================================================================
# BASE
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


# =============================================================================
# SECURITY
# =============================================================================

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]


# =============================================================================
# DATABASE
# =============================================================================

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}


# =============================================================================
# MIDDLEWARE
# =============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]


# =============================================================================
# STATIC FILES
# =============================================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",,
    },
}
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# =============================================================================
# MEDIA FILES
# =============================================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# =============================================================================
# WAGTAIL
# =============================================================================

WAGTAILADMIN_BASE_URL = os.getenv(
    "WAGTAILADMIN_BASE_URL",
    "https://aromire-eko-backend.onrender.com",
)


# =============================================================================
# BREVO
# =============================================================================

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "").strip()
BREVO_DEFAULT_LIST_ID = os.getenv("BREVO_DEFAULT_LIST_ID", "").strip()


# =============================================================================
# CLOUDINARY ENV VALUES
# =============================================================================

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "").strip()
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "").strip()
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "").strip()


# =============================================================================
# SECURITY HEADERS
# =============================================================================

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = False

X_FRAME_OPTIONS = "DENY"


# =============================================================================
# LOCAL OVERRIDES
# =============================================================================

try:
    from .local import *
except ImportError:
    pass
