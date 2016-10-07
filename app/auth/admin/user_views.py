#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, g
from flask.ext.babel import lazy_gettext,gettext
from flask.ext.login import login_required

from app.utils import admin_required
from app.data.models.user import User
from app.public.forms import EditUserForm
from . import admin


@admin.route('/user/list', methods=['GET', 'POST'])
@login_required
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


@admin.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def user_edit(id):
    user = User.query.filter_by(id=id).first_or_404()
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        user.update()
        flash(gettext('User {username} edited').format(username=user.username),'success')
    return render_template('user-edit.html', form=form, user=user)


@admin.route('/user/delete/<int:id>', methods=['GET'])
@admin_required
def user_delete(id):
    user = User.query.filter_by(id=id).first_or_404()
    user.delete()
    flash(gettext('User {username} deleted').format(username=user.username),'success')
    return redirect(url_for('.user_list'))
