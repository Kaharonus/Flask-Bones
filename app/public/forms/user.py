#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from flask_wtf import Form
from flask_babel import gettext,lazy_gettext
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from app.data.models import User
from app.fields import Predicate

def username_is_available(username):
    if not User.if_exists(username):
        return True
    return False

def email_is_available(email):
    if not User.if_exists_email(email):
        return True
    return False

def safe_characters(s):
    " Only letters (a-z) and  numbers are allowed for usernames and passwords. Based off Google username validator "
    if not s:
        return True
    return re.match(r'^[\w]+$', s) is not None

class UserForm(Form):
    username = StringField(lazy_gettext('Username'), validators=[
        Predicate(safe_characters, message=lazy_gettext("Please use only letters (a-z) and numbers")),
        Predicate(username_is_available,message=lazy_gettext("An account has already been registered with that username. Try another?")),
        Length(min=2, max=128, message=lazy_gettext("Please use between 2 and 128 characters")),
        InputRequired(message=lazy_gettext("You can't leave this empty!"))])

    email = StringField(lazy_gettext('Email'), validators=[
        Email(message=lazy_gettext('Please enter a valid email address')),
        Length(min=0, max=128, message=lazy_gettext("Please use under 128 characters")),
        Predicate(email_is_available,message=lazy_gettext("An account has already been registered with that email. Try another?"))])

    jmeno = StringField(lazy_gettext('First Name'), validators=[
        Length(min=0, max=128, message=lazy_gettext("Please use under 128 characters")),
        Predicate(safe_characters, message=lazy_gettext("Please use only letters (a-z) and numbers")),
        #InputRequired(message=lazy_gettext("You can't leave this empty!"))
    ])
    prijmeni = StringField(lazy_gettext('Surname'), validators=[
        Length(min=0, max=128, message=lazy_gettext("Please use under 128 characters")),
        Predicate(safe_characters, message=lazy_gettext("Please use only letters (a-z) and numbers")),
        #InputRequired(message=lazy_gettext("You can't leave this empty!"))
    ])
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class RegisterUserForm(UserForm):
    password = PasswordField(lazy_gettext('Password'),validators=[
        InputRequired(message=lazy_gettext("You can't leave this empty!")),
        EqualTo('confirm',message=lazy_gettext('Passwords must match.')),
        Predicate(safe_characters, message=lazy_gettext("Please use only letters (a-z) and numbers")),
        Length(min=2, max=128, message=lazy_gettext("Please use between 2 and 128 characters"))])

    confirm = PasswordField(lazy_gettext('Confirm Password'), validators=[
        InputRequired(message=lazy_gettext("You can't leave this empty!"))])

    accept_tos = BooleanField(lazy_gettext('I accept the TOS'), validators=[
        InputRequired(message=lazy_gettext("You can't leave this empty!"))])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None


class EditUserForm(UserForm):
    username = StringField(lazy_gettext('Username'))
    is_sadmin = BooleanField(lazy_gettext('Admin'))
    active = BooleanField(lazy_gettext('Activated'))
    email = StringField(lazy_gettext('Email'), validators=[
        Email(message=lazy_gettext('Please enter a valid email address')),
        Length(min=0, max=128, message=lazy_gettext("Please use under 128 characters"))])


class EditProfileForm(UserForm):
    username = StringField(lazy_gettext('Username'))
    email = StringField(lazy_gettext('Email'), validators=[
        Email(message=lazy_gettext('Please enter a valid email address')),
        Length(min=0, max=128, message=lazy_gettext("Please use under 128 characters"))])