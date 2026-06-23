
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "").strip()
BREVO_DEFAULT_LIST_ID = os.getenv("BREVO_DEFAULT_LIST_ID")

from .base import *
# it might look like one of these



# or

# or

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ttfq)mytgx7x203=jb=sijt41c^7zg*@i3o-@gp&5n3s1ky73%"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'home': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
try:
    from .local import *
except ImportError:
    pass
