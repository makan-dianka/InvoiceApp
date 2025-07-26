from pathlib import Path
import dotenv
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv.load_dotenv(BASE_DIR / '.env')

ENV = os.getenv('ENV', 'development')

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = bool(int(os.getenv('DEBUG', 0)))

ALLOWED_HOSTS = []
if DEBUG is False:
   ALLOWED_HOSTS.extend(os.getenv('ALLOWED_HOSTS').split(','))



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',

    'accounts.apps.AccountsConfig',
    'factures.apps.FacturesConfig',
    'payment.apps.PaymentConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'accounts.middleware.UserAccessMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DB'] if ENV=='prod' else os.environ['DBTEST'],
        'USER': os.environ['USER'],
        'PASSWORD': os.environ['PASSWORD'],
        'HOSTS': os.environ['HOSTS'],
        'PORT': os.environ['PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'

STATIC_ROOT = (os.path.join(BASE_DIR, 'staticfiles'))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'
AUTHENTICATION_BACKENDS = ['accounts.backends.EmailBackend']


if ENV == 'prod':
    STRIPE_PRIVATE_KEY = os.getenv('STRIPE_PRIVATE_LIVE_KEY')
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_LIVE_KEY')
else:
    STRIPE_PRIVATE_KEY = os.getenv('STRIPE_PRIVATE_TEST_KEY')
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_TEST_KEY')


# mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'ssl0.ovh.net'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

EMAIL_CC = os.getenv('EMAIL_CC')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')



if DEBUG is False:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(lineno)s %(message)s',
            },

            'simple': {
                'format': '%(levelname)s %(message)s',
            },
        },

        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
        },

        'handlers': {

            'debugger': {
                'filename' :  os.path.join(BASE_DIR, 'logs/debugger.log'),
                'filters': ['require_debug_false'],
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'verbose',
                'backupCount' : 5,
                'maxBytes' : 1024*1024*50,
                'encoding' : 'utf8',
                'level': 'DEBUG',
            },

        },

        'loggers': {

            'debug_log': {
                'handlers': ['debugger'],
                'level': 'DEBUG',
            },
        }
    }