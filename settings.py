# coding=utf-8
import os

import dotenv
from getenv import env

from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

dotenv.read_dotenv(os.path.join(PROJECT_ROOT, env('PROJECT_ENV_FILE', 'server/.env')))

DEBUG = env("DEBUG")
DEBUG_TOOLBAR_PATCH_SETTINGS = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
SESSION_ENGINE = "django.contrib.sessions.backends.file"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Sofia'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'bg'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


EMAIL_HOST = 'localhost'
ALLOWED_HOSTS = ['.obshtestvo.bg']
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']


STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "upload")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/upload/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
SASS_BINARY_PATH = env("SASS_BINARY_PATH")
IS_PROCESS_RUNNING_SCRIPT = env("IS_PROCESS_RUNNING_SCRIPT", os.path.join(PROJECT_ROOT, 'server/is_process_running_by_keyword.sh'))
COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'web.static_helpers.SassFilter'),
    ('text/x-scss', 'web.static_helpers.SassFilter'),
)

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = not DEBUG
COMPRESS_JS_FILTERS = [] if DEBUG else ['compressor.filters.jsmin.JSMinFilter']
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter'] if DEBUG else ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']

# Make this unique, and don't share it with anybody.
SECRET_KEY = env("SECRET_KEY")

DATABASES = {
    'default': {
        # CREATE DATABASE obshtestvo CHARACTER SET utf8 COLLATE utf8_general_ci;
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env("DATABASE_NAME"), # Or path to database file if using sqlite3.
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASS"),
        # 'HOST': '127.0.0.1',
        # 'PORT': 3307,
    }
}

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'restful.middleware.HttpMergeParameters',
    'restful.middleware.HttpMethodOverride',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Before using CSRF make sure it's ONLY enabled when user is logging in or already logged in via cookies
    # Make sure it's not enabled for RESTful requests authenticated via Basic, Digest or OAuth
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'restful.error_handler.ErrorHandler',
    'restful.middleware.ResponseFormatDetection',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'server.wsgi.application'

TEMPLATE_DIRS = (
# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'assetstack',
    'web',
    "projects",
    'django_object_actions',
    'suit',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    "restful",
    "auth",
    "login",
    'reversion',
    "compressor",
    "pagedown",
    'guardian',
    "south",
)
if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
    MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES

    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(PROJECT_ROOT, 'server/mail')

ANONYMOUS_USER_ID = -1
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django-errors.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

MEMBER_POSITIONS = {
    "design": "дизайн",
    "photography": "фотография",
    "illustrations": "илюстрации",
    "accounting": "счетоводство",
    "law": "юридически знания",
    "fund gathering": "фондонабиране",
    "code": "код",
    "business analysis": "бизнес анализа",
    "copyright": "копирайт",
    "pr": "PR",
    "marketing": "маркетинг",
    "ideas": "идеи",
    "donation": "дарение",
}
FAKE_DB = SortedDict()
FAKE_DB["openparliament"] = {
    "name": "Следи парламента",
    "name_full": "Следи парламента",
    "preview": "openparliament.png",
    "fb_group": "https://www.facebook.com/groups/obshtestvo.parlament/",
    "repo": "https://github.com/obshtestvo/rating-gov-representatives",
    "homepage": 1,
    "slug": "openparliament"
}
FAKE_DB["pitaigi"] = {
    "name": "Питай ги",
    "name_full": "Питай ги",
    "url": "http://pitaigi.obshtestvo.bg/",
    "preview": "pitaigi.jpg",
    "fb_group": "https://www.facebook.com/groups/pitaigi.bg/",
    "repo": "https://github.com/obshtestvo/alaveteli-bulgaria",
    "homepage": 2,
    "slug": "pitaigi"
}
FAKE_DB["gradame"] = {
    "name": "Grada.me",
    "name_full": "Grada.me (Града ми)",
    "url": "http://www.grada.me/",
    "preview": "gradame.jpg",
    "fb_group": "https://www.facebook.com/groups/obshtestvo.reallife.bug.tracker/",
    "repo": "https://github.com/obshtestvo-idei/real-life-bug-tracker",
    "homepage": 3,
    "slug": "gradame"
}
FAKE_DB["recycle"] = {
    "name": "RE:CYCLE",
    "name_full": "RE:CYCLE",
    "preview": "recycle.jpg",
    "url": "http://recycle.obshtestvo.bg/",
    "fb_group": "https://www.facebook.com/groups/obshtestvo.recycle/",
    "repo": "https://github.com/obshtestvo/recycle",
    "homepage": 4,
    "slug": "recycle"
}
FAKE_DB["knowyourmp"] = {
    "name": "Опознай депутата",
    "name_full": "Alerts",
    "url": "http://deputati.obshtestvo.bg/",
    "preview": "knowyourmp.jpg",
    "fb_group": "https://www.facebook.com/groups/567844279938127/",
    "repo": "https://github.com/obshtestvo/knowyourmp",
    "homepage": 5,
    "slug": "knowyourmp"
}
FAKE_DB["howto"] = {
    "name": "Howto.bg",
    "name_full": "Howto.bg (Как да ... в България)",
    "url": "http://www.howto.bg/",
    "preview": "howto.jpg",
    "homepage": 6,
    "fb_group": "https://www.facebook.com/groups/oficialen.sait.na.grazhdanina.qna/",
    "repo": "rrrrrrrr",
    "slug": "howto"
}
FAKE_DB["alerts"] = {
    "name": "Обществени Известия",
    "name_full": "Alerts",
    "url": "http://alerts.obshtestvo.bg/",
    "preview": "alerts.jpg",
    "repo": "https://github.com/obshtestvo/state-alerts",
    "fb_group": "None",
    "homepage": False,
    "slug": "alerts"
}



SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'django.core.context_processors.request',
    'web.context_processors.public_settings',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GooglePlusAuth',
    'social.backends.open_id.OpenIdAuth',
    'social.backends.email.EmailAuth',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

LOGIN_URL = '/join/'
LOGIN_REDIRECT_URL = '/dashboard/'
URL_PATH = ''
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/userinfo.profile'
]
# SOCIAL_AUTH_EMAIL_FORM_URL = '/signup-email'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'auth.mail.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/email-sent/'
# SOCIAL_AUTH_USERNAME_FORM_URL = '/signup-username'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'
SOCIAL_AUTH_PIPELINE = (
    'auth.pipeline.load_user',
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'auth.pipeline.user_password',
    'auth.pipeline.require_extra_data',
    'social.pipeline.mail.mail_validation',
    # 'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'auth.pipeline.save_extra_data',
    'social.pipeline.social_auth.associate_user', # creates a social user record
    'social.pipeline.social_auth.load_extra_data', # adds provider metadata like "expire" or "id"
    'social.pipeline.user.user_details' # tops up User model fields with what's available in "details" parameter
)

SOCIAL_AUTH_FACEBOOK_KEY = '1489028994643386'
SOCIAL_AUTH_FACEBOOK_SECRET = env("SOCIAL_AUTH_FACEBOOK_SECRET")
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'bg_BG'}
EMAIL_FROM = 'info@obshtestvo.bg'
AUTH_USER_MODEL = 'projects.User'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_education_history', 'user_interests']
LOCALE_PATHS = ['locale',]
#
SUIT_CONFIG = {
    'SEARCH_URL': '',
    'ADMIN_NAME': 'Obshtestvo.bg',
    'MENU': (
        {'label': _('community'), 'icon':'icon-user', 'models': (
            {'model': 'projects.user', 'label': _('users')},
            {'model': 'projects.userprojectpause', 'label': _('project pauses')},
            {'model': 'projects.useractivity', 'label': _('activities')},
            {'model': 'default.usersocialauth', 'label': _('social auth')},
            {'model': 'default.association', 'label': _('social associations')},
            'auth.group',
        )},
        {'label': _('Partnership & Events'), 'icon':'icon-heart', 'models': (
            {'model': 'projects.organisation', 'label': _('all organisations')},
            {'model': 'projects.sponsororg', 'label': _('sponsorship')},
            {'model': 'projects.partnerorg', 'label': _('partners')},
            {'model': 'projects.event', 'label': _('events')},
        )},
        {
            'app': 'projects',
            'label': _('projects'),
            'icon': 'icon-tasks',
            'models': (
                'project',
                {'model': 'projectactivity', 'label': _('activities')},
                # {'model': 'projectactivitytemplate', 'label': _('activity templates')},
                'task',
            )
        },
        {
            'label': _('settings'),
            'icon': 'icon-cog',
            'models': (
                {'model': 'projects.membertype', 'label': _('member types')},
                {'model': 'projects.organisationtype', 'label': _('organisation types')},
                {'model': 'projects.skill', 'label': _('skills')},
                {'model': 'projects.skillgroup', 'label': _('skill groups')},
            )
        },
    )
}
PUBLIC_SETTINGS = ['SOCIAL_AUTH_FACEBOOK_KEY', 'SOCIAL_AUTH_FACEBOOK_SCOPE']
