#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, g, abort
from flask_babel import lazy_gettext,gettext
from flask_login import login_required

from app.utils import admin_required, crypt
from app.data.models import Group, User, U_G_Association
from app.public.forms import EditGroupForm
from . import admin
import json
from app.utils import fake_group


@admin.route('/group/list', methods=['GET', 'POST'])
@admin_required
def group_list():

    from app.data import DataTable
    datatable = DataTable(
        model=Group,
        columns=[],
        sortable=[Group.group_name, Group.created_ts],
        searchable=[Group.group_name],
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
        flash(gettext('Group {name} edited').format(name=group.name), 'success')
    return render_template('group-edit.html', form=form, group=group)


@admin.route('/group/delete/<str_hash>', methods=['GET'])
@admin_required
def group_delete(str_hash):
    id = int(float(crypt(str_hash, decrypt=True)))
    group = Group.query.filter_by(id=id).first_or_404()
    group.delete()
    flash(gettext('Group {name} deleted').format(name=group.name),'success')
    return redirect(url_for('.group_list'))


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User) or isinstance(obj, Group):
            return obj.to_json()
        return json.JSONEncoder.default(self, obj)


@admin.route('/group/edit_users/', methods=['GET', 'POST'])
@admin_required
def group_edit_users():
    groups = Group.query.all()
    array = json.dumps(groups, cls=CustomEncoder)
    return render_template('group_add_users.html', array=array)


@admin.route('/group/edit_users_submit/', methods=['POST'])
@admin_required
def group_edit_users_submit():
    if request.method != "POST":
        return "Only POST requests allowed"
    data = json.loads(request.values.get('data'))
    userdata = [User.query.filter_by(id=row[0]).first() for row in data.get('data')]
    group = Group.query.filter_by(name=data.get('group')).first_or_404()
    userlist = User.find_in_group(group.id)
    for user in User.query.all():
        if user in userlist and user not in userdata:
            group.remove_user(user)
        if user not in userlist and user in userdata:
            group.add_user(user)
    return "ok"


@admin.route('/group/_get_users/<group_name>', methods=['GET', 'POST'])
def get_users(group_name):
    group = Group.query.filter_by(name=group_name).first_or_404()
    users = User.query.join(U_G_Association).join(Group).filter(Group.id == group.id).all()
    nonusers = [x for x in User.query.all() if x not in users]
    return json.dumps([{'data': nonusers}, {'data': users}], cls=CustomEncoder)
