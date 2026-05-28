import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# .env configuration
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'dev-secret-change-in-production-immediately'
)

DEBUG = os.getenv('DEBUG', 'False') == 'True'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production').lower()
DEBUG = DEBUG or ENVIRONMENT == 'development'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ============ INSTALLED APPS ============

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'rest_framework',
    'corsheaders',
    
    # Local apps
    'merchants',
    'analytics',
]

# ============ MIDDLEWARE ============

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.tenant.TenantMiddleware',
    'middleware.metrics.PerformanceMetricsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ============ TEMPLATES ============

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ============ DATABASE ============

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres.fcosnsnwktqanfbuphwz'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'aws-1-ap-southeast-2.pooler.supabase.com'),
        'PORT': os.getenv('DB_PORT', '6543'),
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}

# ============ AUTH & PASSWORD ============

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============ INTERNATIONALIZATION ============

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

APPEND_SLASH = False

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ============ REST FRAMEWORK CONFIG ============

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'merchants.views.TransactionPagination',
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'merchants.throttles.MerchantRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'merchant': '60/minute',
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# ============ CORS CONFIGURATION ============

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-merchant-id',
]

# ============ SECURITY SETTINGS ============

SECURE_SSL_REDIRECT = False
PREPEND_WWW = False
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# ============ LOGGING ============

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'merchants': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'analytics': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'middleware': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'