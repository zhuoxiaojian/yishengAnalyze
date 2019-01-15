"""
Django settings for yishengAnalyze project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'yi_sheng_apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'utils'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '78aoyg-89pvti7)gu()7nz+*d!(p9d=fegopuzs8^#83kj*rnt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '192.168.3.33']
#权限配置
AUTH_USER_MODEL = 'users.UserProfile'
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DjangoUeditor',
    'xadmin',
    'crispy_forms',
    'users',
    'menu',
    'systemToken',
    'depart',
    'groupDepart',
    'groupMenu',
    'constant',
    'rest_framework',
    'corsheaders',

    #添加定时任务管理
    'djcelery',
    'systemTask',
    'django_filters',
    'yiShengUser'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',#允许跨域
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'yisheng.yiShengLoginRequestMiddle.SimpleMiddleware',#添加手机端登录app时的拦截认证
]
CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'yishengAnalyze.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'appfront/dist')]
        ,
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


WSGI_APPLICATION = 'yishengAnalyze.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yishengAnalyze_dev',
        'HOST': 'localhost',
        'PORT': 22799,
        'USER': 'root',
        'PASSWORD': '123456'
    },
    'db01': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jeecg',
        'HOST': 'localhost',
        'PORT': 22799,
        'USER': 'root',
        'PASSWORD': '123456'
    },
    'db02': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ysanalyze',
        'HOST': 'localhost',
        'PORT': 22799,
        'USER': 'root',
        'PASSWORD': '123456'
    },
}
# 在models中的class Meta:中指定app_label
# app_label = "app02"
# 配置数据库路由
DATABASE_ROUTERS = ['yishengAnalyze.database_router.DatabaseAppsRouter']
# 设置APP对应的数据库路由表
DATABASE_APPS_MAPPING = {
    #     # example:
    #     # 'app_name':'database_name',
    #     'app02': 'db02',
    #     'app01': 'db01',
    #     'admin': 'db01',
    #     'auth':  'db01',
    #     'contenttypes': 'db01',
    #     'sessions': 'db01',
    'YishengUser': 'db01',
    'verifyCode': 'db01',
    'Optimization': 'db01',
    'Industry': 'db01',
    'FtpUser': 'db01',
    'Contract': 'db01',
    'Channel': 'db01',
    'HelpInstruction': 'db01',
    'HitAvgPrice': 'db01',
    'UserSites': 'db01',


}
# migrate  --database=db01

# **********************缓存设置***************************
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/6",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "123456"
        },
        # 'TIMEOUT': 3600,
    }
}
REDIS_TIMEOUT = 7*24*60*60
DAY_REDIS_TIMEOUT = 24*60*60
CUBES_REDIS_TIMEOUT = 60*60
NEVER_REDIS_TIMEOUT = 365*24*60*60

# **********************session***************************
SESSION_COOKIE_AGE = 3600  # 60分钟
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# from django.core.cache import cache #引入缓存模块
# cache.set('v', '555', 60*60)      #写入key为v，值为555的缓存，有效期30分钟
# cache.has_key('v') #判断key为v是否存在
# cache.get('v')     #获取key为v的缓存


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/


LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'appfront/dist/static'),
]

# debug=False，项目根目录下的static文件夹
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

import datetime
#token有效期
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'utils.ResponsePayloadHanderUtil.jwt_response_payload_handler'
}