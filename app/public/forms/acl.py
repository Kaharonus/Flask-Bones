#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from flask_wtf import Form
from flask_babel import gettext,lazy_gettext
from wtforms import TextField, PasswordField, BooleanField
from wtforms.fields import SelectField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.data.models import Acl, Acl_User
from app.fields import Predicate

def Acl_is_available(topic, user_name):
    if not Acl.if_exists(topic, user_name):
        return True
    return False

def safe_characters(s):
    " Only letters (a-z) and  numbers are allowed for usernames and passwords. Based off Google username validator "
    if not s:
        return True
    return re.match(r'^\/?[\w]+$', s) is not None

class AclForm(Form):
    topic = TextField(lazy_gettext('Topic'), validators=[
        Predicate(safe_characters, message=lazy_gettext("Please use only letters (a-z) and numbers")),
        Predicate(Acl_is_available,message=lazy_gettext("This Acl has already been created. Try another?")),
        Length(min=1, max=128, message=lazy_gettext("Please use between 2 and 30 characters")),
        InputRequired(message=lazy_gettext("You can't leave this empty"))])
    user_name = QuerySelectField('User', query_factory=lambda: Acl_User.query.all())
    rw = SelectField('0', choices=[0, 1, 2])

# class RegisterAclUserForm(AclForm):
#     password = PasswordField(lazy_gettext('Password'), validators=[
#         InputRequired(message=lazy_gettext("You can't leave this empty")),
#         EqualTo('confirm', message=lazy_gettext('Passwords must match.')),
#         Predicate(safe_characters, message=lazy_gettext("Please use only letters (a-z) and numbers")),
#         Length(min=2, max=30, message=lazy_gettext("Please use between 2 and 30 characters"))])
#     # password = PasswordField(lazy_gettext('Password'),validators=[DataRequired(lazy_gettext('This field is required.')),EqualTo('confirm',message=lazy_gettext('Passwords must match.')),Length(min=6, max=20)])
#     confirm = PasswordField(lazy_gettext('Confirm Password'), validators=[
#         InputRequired(message=lazy_gettext("You can't leave this empty"))])
#     # confirm = PasswordField(lazy_gettext('Confirm Password'), validators=[DataRequired(lazy_gettext('This field is required.'))])
#     accept_tos = BooleanField(lazy_gettext('I accept the TOS'), validators=[
#         InputRequired(message=lazy_gettext("You can't leave this empty"))])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

class EditAclForm(AclForm):
    is_admin = BooleanField(lazy_gettext('Admin'))
    active = BooleanField(lazy_gettext('Activated'))
