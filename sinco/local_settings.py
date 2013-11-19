import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

LOCAL = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

ROOT_URLCONF = 'sinco.urls'

SECRET_KEY = 'x7n*m)l+t6jy2b!9^6-kch2p-6iu-90y#&gqc+@u7f@q8l4b76'

STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sinco',
        'USER': 'root',
        'PASSWORD': '3187',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

INSTALLED_APPS = (
	'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'suit',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'flexselect',
    # 'tastypie',
    'tags',
    'sinco.core',
    'south',
    'debug_toolbar',
)
