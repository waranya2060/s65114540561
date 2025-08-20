"""
Django settings for django_end project.

Production configuration (PostgreSQL only).
"""

from pathlib import Path
import os

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------
# Core / Production flags
# ------------------------------------------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'please-change-me-for-production')
DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '202.28.49.122,localhost').split(',')
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED',
    'http://202.28.49.122,https://202.28.49.122'
).split(',')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------
# Installed apps
# ------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'api',
    'crispy_forms',
    # ถ้ามี djangorestframework ให้เปิดบรรทัดด้านล่าง
    # 'rest_framework',
]

# ------------------------------------------------------------
# Middleware
# ------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serve static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Static files via WhiteNoise (hashed, compressed)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ------------------------------------------------------------
# URL / WSGI
# ------------------------------------------------------------
ROOT_URLCONF = 'django_end.urls'
WSGI_APPLICATION = 'django_end.wsgi.application'

# ------------------------------------------------------------
# Templates
# ------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # ใส่ไดเรกทอรี template เพิ่มได้ที่นี่
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'cart_template_tags': 'api.cart_template_tags',
            },
        },
    },
]

# ------------------------------------------------------------
# Database (PostgreSQL only)
# ------------------------------------------------------------
DB_ENGINE = os.getenv('DB_ENGINE', 'postgres')
if DB_ENGINE not in ('postgres', 'postgresql'):
    raise RuntimeError('This deployment is locked to PostgreSQL only')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'studentdb'),
        'USER': os.getenv('DB_USER', 'studentuser'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'studentpass123'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
        # เปิด persistent connections สำหรับ production
        'CONN_MAX_AGE': 60,
    }
}

# ------------------------------------------------------------
# Authentication / Password validation
# ------------------------------------------------------------
AUTH_USER_MODEL = 'api.Users'  # ใช้โมเดล Users ในแอป api

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------
# Static / Media
# ------------------------------------------------------------
# เส้นทาง static ใน production (รวบโดย collectstatic)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ถ้ามีโฟลเดอร์ static ภายในโปรเจกต์ให้อ่านด้วย (ไม่จำเป็นต้องมี)
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------------------------------------
# Django REST Framework (ถ้าใช้งานให้เปิด app ด้วย)
# ------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
