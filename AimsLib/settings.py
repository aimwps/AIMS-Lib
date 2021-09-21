
from django.contrib.messages import constants as messages
from pathlib import Path
import os
from decouple import config
import django_heroku
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'forum',
    'Development',
    'Members',
    'ckeditor',
    'bootstrap_datepicker_plus',
    'embed_video',
    'rest_framework',
    'Benchmark',
    'QuestionGenerator',
    'VideoLecture',
    'WrittenLecture',
    'Paths',
    'ShareContent'
    #'Benchmark'


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AimsLib.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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




WSGI_APPLICATION = 'AimsLib.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
DEFAULT_AUTO_FIELD='django.db.models.AutoField'

# bfg --delete-files myfile.txt


MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info alert-dismissible fade show',
        messages.SUCCESS: 'alert-success alert-dismissible fade show',
        messages.WARNING: 'alert-warning alert-dismissible fade show',
        messages.ERROR: 'alert-danger alert-dismissible fade show',
 }

#django_heroku.settings(locals())
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': "100%",
        'width': "100%",
    },
    'article_editor': {
        'height': "500",
        'width': "100%",
        'toolbar': 'Custom',
        'toolbar_Custom':[
                ['RemoveFormat', 'Source','Cut', 'Copy', 'Paste', 'PasteText','Bold', 'Italic', 'Underline', 'Link', 'Unlink','Table', 'HorizontalRule', 'Smiley', 'SpecialChar',],
                ['Styles', 'Format', 'Font','NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',],
                ],

    },
}
django_heroku.settings(locals())
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

CELERY_BROKER_URL = "redis://:p2d75b7c09d68d70852071884b5b51cc56215e5bda9ef1eaf776bc88eb37ef3ac@ec2-34-242-168-78.eu-west-1.compute.amazonaws.com:15140"
