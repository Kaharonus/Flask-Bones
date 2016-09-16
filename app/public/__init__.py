from flask import Blueprint, g

public = Blueprint('public', __name__, template_folder='templates',url_prefix='/<lang_code>')

@public.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)

@public.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')

from .views import *
