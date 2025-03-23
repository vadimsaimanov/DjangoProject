"""
Django settings for itproger project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'. Здесь записывается полный путь к моему проекту
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret! Секретный ключ, нельзя никому показывать. Перед выгрузкой сайта на сервер ключ поменять
SECRET_KEY = 'django-insecure-zr&i4ec-zq#+53ok84fk=4*hq)uuu29cfw-uq&&^dp_&4lkmm-'

# SECURITY WARNING: don't run with debug turned on in production! Показывает ошибки на сайте
DEBUG = True

ALLOWED_HOSTS = [] #указываем те хосты и домены, чтобы публиковать наш сайт


# Application definition
#список, хранит все установленные приложения в проекте в виде списка
INSTALLED_APPS = [
    'main', #добавили свое приложение для управления ссылками на html шаблоны
    'news', #добавили свое приложение для работы с базой данных sqlite
    'ormsql', #добавили свое приложение для работы с базой данных postgresql
    'django.contrib.admin', #панель админа
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
#промежуточное ПО, плагины или библиотеки, которые обеспечивают безопасность, с сессиями и тд
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'itproger.urls' #основной файл urls
#Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], #возможно понадобиться прописать слово templates внутри скобок
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

WSGI_APPLICATION = 'itproger.wsgi.application' #технология для выгрузки сайта на сервер


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
#прописываем с какой базой данных будем рабаотать по умолчанию встроенная в Django sqlite3
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'djangosql',
        'USER': 'pythonsql',
        'PASSWORD': 'mysecretpassword',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru' #язык для всего приложения

TIME_ZONE = 'UTC' #временная зона

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGIN_REDIRECT_URL = reverse_lazy("main:profile")
LOGIN_REDIRECT_URL = 'profile'  # Перенаправление после успешного входа
LOGOUT_REDIRECT_URL = 'login'   # Перенаправление после выхода

AUTH_USER_MODEL = 'main.UserProfile' #чтобы Django использовал твою кастомную модель пользователя

# settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Использование базы данных для хранения сессий
SESSION_COOKIE_AGE = 1209600  # Время жизни сессии в секундах (2 недели)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Сессия не завершается при закрытии браузера