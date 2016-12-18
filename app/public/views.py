#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app, request, redirect, url_for, render_template, flash, abort,g
from flask_babel import lazy_gettext,gettext
from flask_login import login_user, current_user
from itsdangerous import URLSafeSerializer, BadSignature
from app.extensions import lm
from app.tasks import send_registration_email
from app.data.models.user import User
from app.data.models.acl_user import Acl_User
from .forms import LoginForm, RegisterUserForm, RegisterAclUserForm

from . import public


@lm.user_loader
def load_user(id):
        return User.get_by_id(int(id))


@public.route('/index')
def index():
    return render_template("index.html")


@public.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        flash(gettext('You were logged in as {username}').format(username=form.user.username,),'success')
        return redirect(request.args.get('next') or g.lang_code+'/index')
    return render_template('login.html', form=form)


@public.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = User.create(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password'],
            remote_addr=request.remote_addr,
            jmeno=form.data['jmeno'],
            prijmeni=form.data['prijmeni']
        )

        s = URLSafeSerializer(current_app.secret_key)
        token = s.dumps(user.id)

        send_registration_email.delay(user, token)

        flash(gettext('Sent verification email to {email}').format(email=user.email),'success')
        return redirect(url_for('public.index'))
    return render_template('register.html', form=form)


@public.route('/verify/<token>', methods=['GET'])
def verify(token):
    s = URLSafeSerializer(current_app.secret_key)
    try:
        id = s.loads(token)
    except BadSignature:
        abort(404)

    user = User.query.filter_by(id=id).first_or_404()
    if user.active:
        abort(404)
    else:
        user.active = True
        user.update()

        flash(gettext('Registered user {username}. Please login to continue.').format(username=user.username,),'success')
        return redirect(url_for('public.login'))


@public.route('/registerAclUser', methods=['GET', 'POST'])
def register_acl_user():
    form = RegisterAclUserForm()
    if form.validate_on_submit():
        aclUser = Acl_User.create(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password']
        )

        s = URLSafeSerializer(current_app.secret_key)
        token = s.dumps(aclUser.id)

        send_registration_email.delay(aclUser, token)

        flash(gettext('Sent verification email to {email}').format(email=aclUser.email), 'success')
        return redirect(url_for('public.index'))
    return render_template('register_acl_user.html', form=form)
