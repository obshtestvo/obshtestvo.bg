# coding=utf-8
# Django settings for mysite project.
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
from server.settings_app import *

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
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

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
    'restful.middleware.ResponseFormatDetection',
    'restful.error_handler.ErrorHandler',
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
    'reversion',
    'guardian',
    "compressor",
    "pagedown",
)
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
    "name": "Отворен Парламент",
    "name_full": "Отворен Парламент",
    "preview": "openparliament.png",
    "fb_group": "https://www.facebook.com/groups/obshtestvo.parlament/",
    "repo": "https://github.com/obshtestvo/rating-gov-representatives",
    "homepage": 1,
    "slug": "openparliament"
}
FAKE_DB["pitaigi"] = {
    "name": "Pitaigi.bg",
    "name_full": "Pitaigi.bg (Питай ги)",
    "url": "http://foi.obshtestvo.bg/",
    "preview": "pitaigi.jpg",
    "fb_group": "https://www.facebook.com/groups/pitaigi.bg/",
    "repo": "https://github.com/obshtestvo/alaveteli-bulgaria",
    "homepage": 2,
    "slug": "pitaigi"
}
FAKE_DB["grada.me"] = {
    "name": "Grada.me",
    "name_full": "Grada.me (Града ми)",
    "url": "http://www.grada.me/",
    "preview": "gradame.jpg",
    "fb_group": "https://www.facebook.com/groups/obshtestvo.reallife.bug.tracker/",
    "repo": "https://github.com/obshtestvo-idei/real-life-bug-tracker",
    "homepage": 3,
    "slug": "grada.me"
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

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/done/'
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
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'auth.pipeline.require_email',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.user.get_username',
    # 'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user', # creates a social user record
    'social.pipeline.social_auth.load_extra_data', # adds provider metadata like "expire" or "id"
    'social.pipeline.user.user_details' # tops up User model fields with what's available in "details" parameter
)

SOCIAL_AUTH_FACEBOOK_KEY = '587878011289347'
SOCIAL_AUTH_FACEBOOK_SECRET = 'f648ffde60c93685060ae1152816108d'
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'bg_BG'}
EMAIL_FROM = 'info@obshtestvo.bg'
AUTH_USER_MODEL = 'projects.User'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_education_history', 'user_interests']

SUIT_CONFIG = {
    'ADMIN_NAME': 'Obshtestvo.bg',
    'MENU': (
        {'label': _('coordination'), 'icon':'icon-heart', 'models': (
            {'model': 'projects.member', 'label': _('members')},
            {'model': 'projects.membertype', 'label': _('member types')},
            {'model': 'projects.skill', 'label': _('skills')},
        )},
        {'label': _('Partners & Funding'), 'icon':'icon-bookmark', 'models': (
            {'model': 'projects.organisation', 'label': _('organisations')},
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
        {'label': _('System users'), 'icon':'icon-user', 'models': (
            {'model': 'projects.user', 'label': _('users')},
            {'model': 'projects.userprojectpause', 'label': _('project pauses')},
            {'model': 'projects.useractivity', 'label': _('activities')},
            'auth.group',
        )},
    )
}