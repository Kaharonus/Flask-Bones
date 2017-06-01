#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import Form
from flask_babel import gettext, lazy_gettext
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length
from pyvat import check_vat_number
from app.data.models import Group, Company

class CompanyForm(Form):
    company_name = StringField(lazy_gettext('Organization Name'), validators=[DataRequired(lazy_gettext("You can't leave this empty!")), Length(min=2, max=128)])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

class RegisterCompanyForm(CompanyForm):
    address = StringField(lazy_gettext('Address'), validators=[DataRequired(lazy_gettext("You can't leave this empty!")), Length(min=2, max=128)])
    state = StringField(lazy_gettext('State'), validators=[DataRequired(lazy_gettext("You can't leave this empty!")), Length(min=2, max=64)])
    contact_person = StringField(lazy_gettext('Contact Person'), validators=[Length(max=64)])
    phone_number = StringField(lazy_gettext('Phone number'), validators=[DataRequired(lazy_gettext("You can't leave this empty!")), Length(max=16)])
    website = StringField(lazy_gettext('Organization website'), validators=[Length(max=64)])
    #vatnumber = StringField(lazy_gettext('VAT number'), validators=[DataRequired(lazy_gettext("You can't leave this empty!")), Length(max=32), check_vat_number])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        company = Company.query.filter_by(company_name=self.company_name.data).first()
        if company:
            self.company_name.errors.append(gettext('Organization name already registered'))
            return False

        self.company = company
        return True


class EditCompanyForm(CompanyForm):
    pass
