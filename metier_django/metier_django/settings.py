"""
Django settings for metier_django project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#evite de prefixer les package core et user par serveurweb.
# PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
# ROOT_DIR = os.path.dirname(PROJECT_DIR)
# APPS_DIR = os.path.realpath(os.path.join(ROOT_DIR, 'serveurweb'))
# sys.path.append(APPS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rud%1fz_m+8fxgn*%ysdttip(o!w3480^+2_4n&41fqrv#=9@u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
                 socket.gethostname(), # nom serveur
                 'localhost',
                 ]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_xmlrpc',
    'rest_framework',
    'serveurweb',
    'serveurweb.user', #pour avoir le path au html user/templates/user
    'serveurweb.core', #pour avoir le path au html core/templates/core
    'serveurXMLRPC',
    'serveurREST',
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

ROOT_URLCONF = 'metier_django.urls'

WSGI_APPLICATION = 'metier_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': { # ne sert à rien mais doit être définit : lors de migrations création d'une table django_migrations vide
        'ENGINE'    : 'django.db.backends.sqlite3',
        'NAME'      : '/home/stefano/test',
        'USER'      : '',
        'PASSWORD'  : '',
        'HOST'      : 'localhost',
        'PORT'      : '5432',
    },
#     'postgres': {
#         'ENGINE'    : 'django.db.backends.postgresql_psycopg2',
#         'NAME'      : 'test',
#          'USER'      : '',
#          'PASSWORD'  : '',
#          'HOST'      : 'localhost',
#          'PORT'      : '5432',
#     },
#     'sqlite': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': '/home/stefano/test',
#     }
}

# DATABASE_ROUTERS = ['metier_django.routersDB.SqliteRouter']

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/' # http:/localhost:8000/static/
STATIC_ROOT = BASE_DIR + '/STATIC/' #répertoire ou les fichiers static se trouve pour la prod


# Templates location
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# register methods XML-RPC server
XMLRPC_METHODS = (('serveurXMLRPC.views.afficherMainWindow',    'afficherMainWindow'),
                  ('serveurXMLRPC.views.listerArticles',        'listerArticles'),
                  ('serveurXMLRPC.views.supprimerArticle',      'supprimerArticle'),
                  ('serveurXMLRPC.views.ajouterArticle',        'ajouterArticle'),
                  ('serveurXMLRPC.views.modifierArticle',       'modifierArticle'),)        

#SSL
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# wsgi scheme
os.environ['wsgi.url_scheme'] = 'http'

LOGIN_URL = '/serveurweb/user/connexion/'
LOGIN_REDIRECT_URL = '/serveurweb/'