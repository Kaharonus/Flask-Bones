#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, g
from flask_babel import lazy_gettext,gettext
from flask_login import login_required

from app.utils import admin_required, crypt
from app.data.models import Group, User
from app.public.forms import EditGroupForm
from . import admin
import json


@admin.route('/group/list', methods=['GET', 'POST'])
@admin_required
def group_list():

    from app.data import DataTable
    datatable = DataTable(
        model=Group,
        columns=[],
        sortable=[Group.nazev, Group.created_ts],
        searchable=[Group.nazev],
        filterable=[],
        limits=[25, 50, 100],
        request=request
    )

    if g.pjax:
        return render_template(
            'groups.html',
            datatable=datatable
        )

    return render_template(
        'group-list.html',
        datatable=datatable
    )


@admin.route('/group/edit/<str_hash>', methods=['GET', 'POST'])
@admin_required
def group_edit(str_hash):
    id = int(float(crypt(str_hash, decrypt=True)))
    group = Group.query.filter_by(id=id).first_or_404()
    form = EditGroupForm(obj=group)
    if form.validate_on_submit():
        form.populate_obj(group)
        group.update()
        flash(gettext('Group {nazev} edited').format(nazev=group.nazev),'success')
    return render_template('group-edit.html', form=form, group=group)


@admin.route('/group/delete/<str_hash>', methods=['GET'])
@admin_required
def group_delete(str_hash):
    id = int(float(crypt(str_hash, decrypt=True)))
    group = Group.query.filter_by(id=id).first_or_404()
    group.delete()
    flash(gettext('Group {nazev} deleted').format(nazev=group.nazev),'success')
    return redirect(url_for('.group_list'))


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User) or isinstance(obj, Group):
            return obj.to_json()
        return json.JSONEncoder.default(self, obj)


@admin.route('/group/add/', methods=['GET', 'POST'])
def group_add_user():
    groups = Group.query.all()
    pole = json.dumps(groups, cls=CustomEncoder)
    return render_template('group_add_users.html', pole=pole)

@admin.route('/group/_get_users', methods=['POST'])
def get_users():
    pass