#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, g, current_app
from flask_babel import lazy_gettext,gettext
from flask_login import login_required, current_user

from app.tasks import send_registration_email
from itsdangerous import URLSafeSerializer
from app.utils import admin_required, crypt
from app.data.models.user import User
from app.public.forms import EditUserForm
from . import admin
from app.public.forms import RegisterUserForm


@admin.route('/user/list', methods=['GET', 'POST'])
@admin_required
def user_list():

    from app.data import DataTable
    datatable = DataTable(
        model=User,
        columns=[User.remote_addr],
        sortable=[User.username, User.email, User.created_ts],
        searchable=[User.username, User.email],
        filterable=[User.active],
        limits=[10, 25, 50, 100],
        request=request
    )

    if g.pjax:
        return render_template(
            'users.html',
            datatable=datatable,
            stats=User.stats()
        )

    return render_template(
        'user-list.html',
        datatable=datatable,
        stats=User.stats()
    )


@admin.route('/user/edit/<str_hash>', methods=['GET', 'POST'])
@admin_required
def user_edit(str_hash):
    id = int(float(crypt(str_hash, decrypt=True)))
    user = User.query.filter_by(id=id).first_or_404()
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        if User.if_exists_email(form.email._value()) and user.email!=form.email._value():
            flash(gettext("An account has already been registered with that email. Try another?"), 'warning')
            return render_template('user-edit.html', form=form, user=user)
        if not user.username == form.username._value():
            flash(gettext("You little rebel! I like you!"), 'warning')
            return render_template('user-edit.html', form=form, user=user)
        form.populate_obj(user)
        user.commit()
        flash(gettext('User {username} edited').format(username=user.username),'success')
    return render_template('user-edit.html', form=form, user=user)


@admin.route('/user/delete/<str_hash>', methods=['GET'])
@admin_required
def user_delete(str_hash):
    id = int(float(crypt(str_hash, decrypt=True)))
    user = User.query.filter_by(id=id).first_or_404()
    user.delete()
    flash(gettext('User {username} deleted').format(username=user.username),'success')
    if current_user.id==id:
        return redirect(url_for('public.index'))
    return redirect(url_for('.user_list'))


@admin.route('/user/create/', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = User.create(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password'],
            remote_addr=request.remote_addr,
            first_name=form.data['first_name'],
            last_name=form.data['last_name']
        )

        s = URLSafeSerializer(current_app.secret_key)
        token = s.dumps(user.id)

        # send_registration_email.delay(user, api_key)

        # flash(gettext('Sent verification email to {email}').format(email=user.email),'success')
        return redirect(url_for('.user_list'))
    return render_template('register.html', form=form)