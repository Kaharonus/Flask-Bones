#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from flask_wtf import Form
from flask_babel import gettext,lazy_gettext
from wtforms import TextField, PasswordField, BooleanField, validators
from wtforms.fields import SelectField, IntegerField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.data.models import Acl, Ctecka
from app.fields import Predicate


def Acl_is_available(topic):
     if not Acl.if_exists(topic):
         return True
     return False


def safe_characters(s):
    " Only letters (a-z) and  numbers are allowed for usernames and passwords. Based off Google username validator "
    if not s:
        return True
    return re.match(r'^\/[\w]+$', s) is not None


class AclForm(Form):
    topic = TextField(lazy_gettext('Topic'), default="/", validators=[
        Predicate(safe_characters, message=lazy_gettext("Please use only letters (a-z) and numbers with a '/' at the start")),
        Length(min=1, max=128, message=lazy_gettext("Please use between 2 and 30 characters")),
        InputRequired(message=lazy_gettext("You can't leave this empty"))])
    rw = SelectField('Permissions', choices=[('0', 'No permissions'), ('1', 'Read Only'), ('2', 'Read and Write')])
    #rw = IntegerField('RW', [validators.NumberRange(message='Range should be between 0 and 2.', min=0, max=2)])


class RegisterAclForm(AclForm):
    ctecka = QuerySelectField('Ctecka', query_factory=lambda: Ctecka.query.all(), get_label=lambda a: a.username)
    private = BooleanField(lazy_gettext('Private topic'))
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class EditAclForm(AclForm):
    user_name = TextField(lazy_gettext('Username'))
    topic = TextField(lazy_gettext('Topic'), default="/", validators=[
        Predicate(safe_characters,
                  message=lazy_gettext("Please use only letters (a-z) and numbers with a '/' at the start")),
        Length(min=1, max=128, message=lazy_gettext("Please use between 2 and 30 characters")),
        InputRequired(message=lazy_gettext("You can't leave this empty"))])