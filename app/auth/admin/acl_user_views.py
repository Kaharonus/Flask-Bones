#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, g, current_app
from flask_babel import lazy_gettext,gettext
from flask_login import login_required
from itsdangerous import URLSafeSerializer
from app.tasks import send_registration_email
from app.utils import admin_required
from app.data.models.acl_user import Acl_User
from app.public.forms import EditAclUserForm, RegisterAclUserForm
from . import admin


@admin.route('/acl_user/list', methods=['GET', 'POST'])
@login_required
def acl_user_list():

    from app.data import DataTable
    datatable = DataTable(
        model=Acl_User,
        columns=[],
        sortable=[Acl_User.username, Acl_User.email],
        searchable=[Acl_User.username, Acl_User.email],
        filterable=[Acl_User.active],
        limits=[10, 25, 50, 100],
        request=request
    )

    if g.pjax:
        return render_template(
            'acl-users.html',
            datatable=datatable
        )

    return render_template(
        'acl-user-list.html',
        datatable=datatable
    )


@admin.route('/acl_user/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def acl_user_edit(id):
    acl_user = Acl_User.query.filter_by(id=id).first_or_404()
    form = EditAclUserForm(obj=acl_user)
    if form.validate_on_submit():
        form.populate_obj(acl_user)
        acl_user.update()
        flash(gettext('User {username} edited').format(username=acl_user.username),'success')
    return render_template('acl-user-edit.html', form=form, user=acl_user)


@admin.route('/acl_user/delete/<int:id>', methods=['GET'])
@admin_required
def acl_user_delete(id):
    acl_user = Acl_User.query.filter_by(id=id).first_or_404()
    acl_user.delete()
    flash(gettext('User {username} deleted').format(username=acl_user.username),'success')
    return redirect(url_for('.acl_user_list'))


@admin.route('/register_acl_user', methods=['GET', 'POST'])
def register_acl_user():
    form = RegisterAclUserForm()
    if form.validate_on_submit():
        aclUser = Acl_User.create(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password'],
            firma_id=form.data['firma_id'].id
        )

        s = URLSafeSerializer(current_app.secret_key)
        token = s.dumps(aclUser.id)

        send_registration_email.delay(aclUser, token)

        flash(gettext('Sent verification email to {email}').format(email=aclUser.email), 'success')
        return redirect(url_for('public.index'))
    return render_template('register_acl_user.html', form=form)