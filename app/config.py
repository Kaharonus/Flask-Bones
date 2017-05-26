#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from logging import INFO

class base_config(object):
    """Default configuration options."""
    SITE_NAME = 'Flask Bones'
    BABEL_DEFAULT_LOCALE='cs'
    #SERVER_NAME = os.environ['SERVER_NAME']
    #SECRET_KEY = os.environ['SECRET_KEY']
#    SERVER_NAME="localhost:5000"
    SERVER_NAME="localhost:5000"

    SECRET_KEY="sdfsdfsdgwerter346354"

    CYPHER_KEY = bytes(os.urandom(32))

    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '355274304837834',
            'secret': 'e36842e26ee80b71d6350f86d5fa3595'
        },
        'twitter': {
            'id': 'zD1qhPjJNvWGHFuslq4gtB38O',
            'secret': 'ky8avR4bFv1TGXPle2nrl5rfIFWoYfYPVSMoiCO5KJYn9U4vmR'
        }
    }

    #MAIL_SERVER = os.environ['MAILCATCHER_PORT_1025_TCP_ADDR']
    #MAIL_PORT = os.environ['MAILCATCHER_PORT_1025_TCP_PORT']
    MAIL_PORT="1025"
    MAIL_SERVER="localhost"
    #REDIS_HOST = os.environ['REDIS_PORT_6379_TCP_ADDR']
    #REDIS_PORT = os.environ['REDIS_PORT_6379_TCP_PORT']
    REDIS_PORT="6379"
    REDIS_HOST="localhost"
    #BROKER_URL = 'redis://{}:{}'.format(REDIS_HOST, REDIS_PORT)
    BROKER_URL='redis://localhost:6379/0'
    #BROKER_PORT='6379'
    #BROKER_TRANSPORT='sqlalchemy'
    BROKER_BACKEND = BROKER_URL

    #CACHE_HOST = os.environ['MEMCACHED_PORT_11211_TCP_ADDR']
    #CACHE_PORT = os.environ['MEMCACHED_PORT_11211_TCP_PORT']
    CACHE_PORT="11211"
    CACHE_HOST="localhost"

    #POSTGRES_HOST = os.environ['DB_PORT_5432_TCP_ADDR']
    #POSTGRES_PORT = os.environ['DB_PORT_5432_TCP_PORT']
    #POSTGRES_USER = os.environ.get('DB_ENV_USER', 'postgres')
    #POSTGRES_PASS = os.environ.get('DB_ENV_PASS', 'postgres')


    POSTGRES_HOST="localhost"
    POSTGRES_USER="postgres"
    POSTGRES_PORT="5432"
    POSTGRES_PASS="passat221"
    POSTGRES_DB = 'flask_bones'

    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (
        POSTGRES_USER,
        POSTGRES_PASS,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB
    )

    SUPPORTED_LOCALES = ['en','cs']

    LOG_FORMAT = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    LOG_FILEPATH = 'logfile.log'
    LOG_LEVEL = INFO


class dev_config(base_config):
    """Development configuration options."""
    DEBUG = True
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = False


class test_config(base_config):
    """Testing configuration options."""
    TESTING = True
    WTF_CSRF_ENABLED = False
