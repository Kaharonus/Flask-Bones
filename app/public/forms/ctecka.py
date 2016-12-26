#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from flask_login import current_user
from flask_wtf import Form
from flask_babel import gettext,lazy_gettext
from wtforms import TextField, PasswordField, BooleanField, validators
from wtforms.fields import SelectField, IntegerField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.data.models import Firma, Ctecka, U_F_Association
from app.fields import Predicate

def Ctecka_is_available(nazev):
     if not Ctecka.if_exists(nazev):
         return True
     return False

def safe_characters(s):
    " Only letters (a-z) and  numbers are allowed for usernames and passwords. Based off Google username validator "
    if not s:
        return True
    return re.match(r'^\/?[\w]+$', s) is not None


class CteckaForm(Form):
    nazev = TextField(lazy_gettext('Nazev'), validators=[
        Predicate(safe_characters, message=lazy_gettext("Please use only letters (a-z) and numbers")),
        Predicate(Ctecka_is_available ,message=lazy_gettext("This ctecka has already been created. Try another?")),
        Length(min=1, max=32, message=lazy_gettext("Please use between 2 and 32 characters")),
        InputRequired(message=lazy_gettext("You can't leave this empty"))])
    firma_id = QuerySelectField('Firma', query_factory=lambda: [Firma.query.filter_by(id=x.firma_id).first()
                                                    for x in U_F_Association.query.filter_by(
                                                    user_id=current_user.id).all()],
                                get_label=lambda a: a.nazev)

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

class EditCteckaForm(CteckaForm):
    nazev = TextField(lazy_gettext('Nazev'))
