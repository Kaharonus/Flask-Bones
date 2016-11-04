#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import Form
from flask_babel import gettext, lazy_gettext
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length

from app.data.models import Group, Firma


class FirmaForm(Form):
    nazev = StringField(lazy_gettext('Organization Name'), validators=[DataRequired(lazy_gettext('This field is required.')), Length(min=2, max=128)])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class RegisterFirmaForm(FirmaForm):
    address = StringField(lazy_gettext('Address'), validators=[DataRequired(lazy_gettext('This field is required')), Length(min=2, max=128)])
    state = StringField(lazy_gettext('State'), validators=[DataRequired(lazy_gettext('This field is required')), Length(min=2, max=64)])
    contact_person = StringField(lazy_gettext('Contact Person'), validators=[Length(max=64)])
    phone_number = StringField(lazy_gettext('Phone number'), validators=[DataRequired(lazy_gettext('This field is required')), Length(max=16)])
    website = StringField(lazy_gettext('Organization website'), validators=[Length(max=64)])
    accept_tos = BooleanField(lazy_gettext('I accept the TOS'), validators=[DataRequired(lazy_gettext('This field is required.'))])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        firma = Firma.query.filter_by(nazev=self.nazev.data).first()
        if firma:
            self.nazev.errors.append(gettext('Organization name already registered'))
            return False

        self.firma = firma
        return True


class EditFirmaForm(FirmaForm):
    pass
