#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from flask_wtf import Form
from flask_babel import gettext, lazy_gettext
from wtforms import StringField, BooleanField
from wtforms.validators import Length, InputRequired
from app.data.models import Group, User
from app.fields import Predicate

def group_is_available(group):
    if group == "admin":
        return False
    if not Group.if_exists(group,User.idfirm):
        return True
    return False

def safe_characters(s):
    " Only letters (a-z) and  numbers are allowed for usernames and passwords. Based off Google username validator "
    if not s:
        return True
    return re.match(r'^[\w]+$', s) is not None

class GroupForm(Form):
    nazev = StringField(lazy_gettext('Group Name'), validators=[
        Predicate(safe_characters, message=lazy_gettext("Please use only letters (a-z) and numbers")),
        Predicate(group_is_available,message=lazy_gettext("A group has already been created with that name. Try another?")),
        Length(min=2, max=30, message=lazy_gettext("Please use between 2 and 30 characters")),
        InputRequired(message=lazy_gettext("You can't leave this empty"))])

class RegisterGroupForm(Form):
    nazev = StringField(lazy_gettext('Group Name'), validators=[
        Predicate(safe_characters, message=lazy_gettext("Please use only letters (a-z) and numbers")),
        Predicate(group_is_available,message=lazy_gettext("A group has already been created with that name. Try another?")),
        Length(min=2, max=30, message=lazy_gettext("Please use between 2 and 30 characters")),
        InputRequired(message=lazy_gettext("You can't leave this empty"))])


class EditGroupForm(GroupForm):
    pass
