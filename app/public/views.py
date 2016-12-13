#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app, request, redirect, url_for, render_template, flash, abort,g
from flask_babel import lazy_gettext,gettext
from flask_login import login_user, current_user
from itsdangerous import URLSafeSerializer, BadSignature
from app.extensions import lm
from app.tasks import send_registration_email
from app.data.models import User, OAuthSignIn, Oauth
from .forms import RegisterUserForm
from .forms import LoginForm
from . import public


@lm.user_loader
def load_user(id):
        return User.get_by_id(int(id))


@public.route('/index')
def index():
    return render_template("index.html")


@public.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('public.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@public.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('public.index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email,jmeno,prijmeni,profile_url,image_url= oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('public.index'))
    ouser = Oauth.query.filter_by(social_id=social_id).first()
    if email is None:
        flash(gettext('We need your email!'), 'warning')
        return redirect(request.args.get('next') or g.lang_code + '/index')
    user = User.find_by_email(email)
    if user is None:
        user = User.create(
            username=social_id,
            email=email,
            password=social_id,
            remote_addr=request.remote_addr,
            jmeno=jmeno,
            prijmeni=prijmeni,
            profile_url=profile_url,
            image_url=image_url
        )
    if not ouser:
        ouser = Oauth(
            user_id=user.id,
            social_id=social_id, nickname=username, email=email,jmeno=jmeno,prijmeni=prijmeni,profile_url=profile_url,image_url=image_url)
        ouser.save()
    login_user(user, True)
    return redirect(url_for('public.index'))


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

        #send_registration_email.delay(user, token)

        #flash(gettext('Sent verification email to {email}').format(email=user.email),'success')
        flash(gettext('An account {username} has been created.').format(username=form.data['username'], ), 'success')
        return redirect(request.args.get('next') or g.lang_code + '/index')
        #return redirect(url_for('public.index'))
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

