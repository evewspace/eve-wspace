# Django settings for WormholeSpace2 project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ('Andrew Austin', 'acaustin@uark.edu'
        # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': 'djangotest',                      # Or path to database file if using sqlite3.
                'USER': 'root',                      # Not used with sqlite3.
                'PASSWORD': '',                  # Not used with sqlite3.
                'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
                'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'
USE_TZ = True
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Change the default login behavior
LOGIN_URL = '/account/login'
LOGIN_REDIRECT_URL ='/'

# Additional locations of static files
STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
# Make this unique, and don't share it with anybody.
SECRET_KEY = '^28avlv8e$sky_08pu926q^+b5&4&5&+ob7ma%v(tn$bg#=&k4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'eveigb.middleware.IGBMiddleware',
)

ROOT_URLCONF = 'evewspace.urls'

TEMPLATE_DIRS = (
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (    
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Uncomment the next line to enable the admin:
        'django.contrib.admin',
        'core',
        'Map',
        'Jabber',
        'Recruitment',
        'SiteTracker',
        'Teamspeak',
        'Cart',
        'API',
        'account',
        'POS',
        'eveigb',
        'autocomplete_light',
        # Uncomment the next line to enable admin documentation:
        # 'django.contrib.admindocs',
)
#Corp API Key
API_CORP_KEY_ID=325904
API_CORP_KEY_VCODE='bbR0lFKHULzUuh7luVJlz22VUl4T4SkZmMLeveunrMcZxPdbwZqMXMffnUXvaRHF'

#Require a registration code to register
ACCOUNT_REQUIRE_REG_CODE=True

# Map Settings

# Number of minutes that a sytem of interest remains flagged
MAP_INTEREST_TIME=30

AUTH_PROFILE_MODULE = 'account.UserProfile'
import django.conf.global_settings as DEFAULT_SETTINGS
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + ('core.context_processors.site', 'eveigb.context_processors.igb',)
# ejabberd auth gateway log settings

import logging

TUNNEL_EJABBERD_AUTH_GATEWAY_LOG = '/tmp/ejabberd.log'
TUNNEL_EJABBERD_AUTH_GATEWAY_LOG_LEVEL = logging.DEBUG

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
                'mail_admins': {
                        'level': 'ERROR',
                        'class': 'django.utils.log.AdminEmailHandler'
                }
        },
        'loggers': {
                'django.request': {
                        'handlers': ['mail_admins'],
                        'level': 'ERROR',
                        'propagate': True,
                },
        }
}
