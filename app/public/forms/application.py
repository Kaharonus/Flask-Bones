#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.data.models import Company
from flask_wtf import Form
from flask_babel import gettext, lazy_gettext
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length
from pyvat import check_vat_number
from app.data.models import Group, Company



class ApplicationForm(Form):
    application_name = StringField(lazy_gettext('Application Name'),
                       validators=[DataRequired(lazy_gettext("You can't leave this empty!")),
                                Length(min=2, max=128)])
    #CList = Company.query.all()
    company_id = SelectField('Company: ', choices=[('1', 'haha')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
