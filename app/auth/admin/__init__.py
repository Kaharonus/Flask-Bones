#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, g

admin = Blueprint('admin', __name__, template_folder='templates',url_prefix='/<lang_code>')

@admin.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)

@admin.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')

from .user_views import *
from .group_views import *
from .firma_views import *