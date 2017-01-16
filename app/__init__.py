#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, g, render_template, request, redirect
from app.data import db
from app.extensions import lm, api, travis, mail, heroku, bcrypt, celery, babel
from app.assets import assets
import app.utils as utils
from app import config
from app.public import public
from app.auth import auth
from app.auth.admin import admin
from app.fields import Predicate
import time
import logging


def create_app(config=config.base_config):
    app = Flask(__name__)
    app.config.from_object(config)

    logger = logging.getLogger()
    formatter = logging.Formatter(config.LOG_FORMAT)
    file_handler = logging.FileHandler(config.LOG_FILEPATH, encoding='utf-8')
    file_handler.setLevel(config.LOG_LEVEL)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    #app.logger.addHandler(file_handler)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_jinja_env(app)

    @babel.localeselector
    def get_locale():
        lang_code = getattr(g, 'lang_code', None)
        if lang_code is None:
            g.lang_code='en'
        return g.lang_code


    @app.before_request
    def before_request():
        g.request_start_time = time.time()
        g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)
        g.pjax = 'X-PJAX' in request.headers

    @app.route('/', methods=['GET','POST'])
    def root():
        lang = request.accept_languages.best_match(config.SUPPORTED_LOCALES)
        return redirect(lang+'/index')

    @app.route('/forceerror')
    def force_error():
        return 1/0

    return app


def register_extensions(app):
    heroku.init_app(app)
    travis.init_app(app)
    db.init_app(app)
    api.init_app(app)
    lm.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    celery.config_from_object(app.config)
    assets.init_app(app)
    babel.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth)
    app.register_blueprint(public)
    app.register_blueprint(admin)


def register_errorhandlers(app):
    def render_error(e):
        code = e.code if hasattr(e, "code") else 500
        if code==500:
            app.logger.error(e)
        else:
            app.logger.info(e)
        return render_template('errors/%s.html' % code), code

    for e in [401, 404, 500]:
        app.errorhandler(e)(render_error)


def register_jinja_env(app):
    app.jinja_env.globals['url_for_other_page'] = utils.url_for_other_page
    app.jinja_env.globals['timeago'] = utils.timeago
    app.jinja_env.globals['crypt'] = utils.crypt
    app.jinja_env.globals['get_oauth'] = utils.get_oauth
