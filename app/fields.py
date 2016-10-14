#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generic form classes and helpers to use throughout the application
"""
from wtforms.validators import ValidationError
from flask_babel import gettext, lazy_gettext

class Predicate(object):

    def __init__(self, f, message=None):
        self.f = f
        self.message = message

    def __call__(self, form, field):
        valid = self.f(field.data)
        if not valid:
            message = self.message or lazy_gettext('Invalid value')
            raise ValidationError(message)