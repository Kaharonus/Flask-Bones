#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.data.models import Company
from flask_wtf import Form
from flask_babel import gettext, lazy_gettext
from wtforms import StringField
#from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email
from pyvat import check_vat_number
from app.data.models import Company


class ApplicationForm(Form):
    application_name = StringField(lazy_gettext('Application Name'),
                       validators=[DataRequired(lazy_gettext("You can\'t leave this empty!")),
                                Length(min=2, max=128)])
    company_id = QuerySelectField(u'Company: ',query_factory=lambda: Company.query.all())
    email = EmailField("Email", validators=[DataRequired(lazy_gettext("You can\'t leave this empty!")), Email(lazy_gettext("You must enter valid email address"))])
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
