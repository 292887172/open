import os

from django.core.urlresolvers import reverse

from conf.commonconf import IS_DEBUG, STATIC_URL_CONF, SESSION_TIMEOUT
from conf.memcacheconf import MEMCACHED_HOST
from conf.mysqlconf import MYSQL_DB, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT
from conf.mysqlconf import MYSQL_USER


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'w3==6tmr=r8&9%#2oh*78f2fq$bbc#%p%0vo3%-t6i4%*c2nq!'

DEBUG = IS_DEBUG

TEMPLATE_DEBUG = IS_DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "app.center",
    "app.home",
    "app.product",
    "app.wiki",
    "app"
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'open.urls'

WSGI_APPLICATION = 'open.wsgi.application'


# 将session直接保存到缓存中（不经过数据库）
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# session超时时间
SESSION_COOKIE_AGE = SESSION_TIMEOUT
# 缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': MEMCACHED_HOST,
        # 超时时间，单位秒
        'TIMEOUT': None,
    }
}

# 使用@login_required后的跳转登录地址
LOGIN_URL = "/center/login"  # reverse("login")
# 登录用户模型
AUTH_USER_MODEL = "center.Account"


# 数据库连接配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": MYSQL_DB,
        "USER": MYSQL_USER,
        "PASSWORD": MYSQL_PWD,
        "HOST": MYSQL_HOST,
        "PORT": MYSQL_PORT,
    }
}

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# 日期时间格式
DATETIME_FORMAT = 'Y-m-d H:i'
DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i'

STATIC_URL = STATIC_URL_CONF

# 静态资源目录配置
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# 模板中用到的类库配置
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    'django.contrib.auth.context_processors.auth',
)

# 系统日志配置-----------------------------Begin-------------------------------------
Log_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        os.path.pardir))
lformat = '%(asctime)s [%(threadName)s:%(thread)d]'
lformat += ' [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': lformat
        },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(Log_ROOT + "/log/", 'default.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'debug_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(Log_ROOT + "/log/", 'debug.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        '': {
            'handlers': ['debug_handler'],
            'level': 'INFO',
            'propagate': True
        },
    }
}
# 系统日志配置-----------------------------End-------------------------------------