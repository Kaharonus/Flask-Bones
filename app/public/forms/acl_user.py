#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from flask_wtf import Form
from flask_babel import gettext,lazy_gettext
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from app.data.models import Acl_User, Firma, U_F_Association
from app.fields import Predicate
from flask_login import current_user
from wtforms.ext.sqlalchemy.fields import QuerySelectField


def username_is_available(username):
    if not Acl_User.if_exists(username):
        return True
    return False

def safe_characters(s):
    " Only letters (a-z) and  numbers are allowed for usernames and passwords. Based off Google username validator "
    if not s:
        return True
    return re.match(r'^[\w]+$', s) is not None

class AclUserForm(Form):
    username = TextField(lazy_gettext('Username'), validators=[
        Predicate(safe_characters, message=lazy_gettext("Please use only letters (a-z) and numbers")),
        Predicate(username_is_available,message=lazy_gettext("An account has already been registered with that username. Try another?")),
        Length(min=2, max=30, message=lazy_gettext("Please use between 2 and 30 characters")),
        InputRequired(message=lazy_gettext("You can't leave this empty"))])
    #username = TextField(lazy_gettext('Username'), validators=[DataRequired(lazy_gettext('This field is required.')), Length(min=2, max=20)])
    email = TextField(lazy_gettext('Email'), validators=[
        Email(message=lazy_gettext('Please enter a valid email address')),
        InputRequired(message=lazy_gettext('You can\'t leave this empty'))])
    #email = TextField(lazy_gettext('Email'), validators=[Email(lazy_gettext('Invalid email address.')), DataRequired(lazy_gettext('This field is required.')), Length(max=128)])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class RegisterAclUserForm(AclUserForm):
    password = PasswordField(lazy_gettext('Password'),validators=[
        InputRequired(message=lazy_gettext("You can't leave this empty")),
        EqualTo('confirm',message=lazy_gettext('Passwords must match.')),
        Predicate(safe_characters, message=lazy_gettext("Please use only letters (a-z) and numbers")),
        Length(min=2, max=30, message=lazy_gettext("Please use between 2 and 30 characters"))])
    #password = PasswordField(lazy_gettext('Password'),validators=[DataRequired(lazy_gettext('This field is required.')),EqualTo('confirm',message=lazy_gettext('Passwords must match.')),Length(min=6, max=20)])
    confirm = PasswordField(lazy_gettext('Confirm Password'), validators=[
        InputRequired(message=lazy_gettext("You can't leave this empty"))])
    firma_id = QuerySelectField('Firma', query_factory=lambda: [Firma.query.filter_by(id=x.firma_id).first()
                                                                for x in U_F_Association.query.filter_by(
                                                                user_id=current_user.id).all()],
                                get_label=lambda a: a.nazev, get_pk=lambda a: a.id)
    #confirm = PasswordField(lazy_gettext('Confirm Password'), validators=[DataRequired(lazy_gettext('This field is required.'))])
    accept_tos = BooleanField(lazy_gettext('I accept the TOS'), validators=[
        InputRequired(message=lazy_gettext("You can't leave this empty"))])

    #accept_tos = BooleanField(lazy_gettext('I accept the TOS'), validators=[DataRequired(lazy_gettext('This field is required.'))])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class EditAclUserForm(AclUserForm):
    is_admin = BooleanField(lazy_gettext('Admin'))
    active = BooleanField(lazy_gettext('Activated'))
