#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_babel import gettext,lazy_gettext
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired

from app.data.models import User


class LoginForm(Form):
    username = TextField(lazy_gettext('Username'), validators=[DataRequired(lazy_gettext('This field is required.'))])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired(lazy_gettext('This field is required.'))])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None


    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append(gettext('Unknown username'))
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append(gettext('Invalid password'))
            return False

        if not self.user.active:
            self.username.errors.append(gettext('User not activated'))
            return False

        return True
