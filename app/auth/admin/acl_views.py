#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, g
from flask_babel import lazy_gettext,gettext
from flask_login import login_required

from app.utils import admin_required
from app.data.models import Acl
from app.public.forms import EditAclForm
from . import admin


@admin.route('/acl/list', methods=['GET', 'POST'])
@admin_required
def acl_list():

    from app.data import DataTable
    datatable = DataTable(
        model=Acl,
        columns=[],
        sortable=[Acl.user_name],
        searchable=[Acl.user_name],
        filterable=[],
        limits=[25, 50, 100],
        request=request
    )

    if g.pjax:
        return render_template(
            'acl.html',
            datatable=datatable
        )

    return render_template(
        'acl-list.html',
        datatable=datatable
    )


@admin.route('/acl/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def acl_edit(id):
    acl = Acl.query.filter_by(id=id).first_or_404()
    form = EditAclForm(obj=acl)
    if form.validate_on_submit():
        form.populate_obj(acl)
        acl.update()
        flash(gettext('Acls of user {jmeno} edited').format(jmeno=acl.user_name),'success')
    return render_template('acl-edit.html', form=form, firma=acl)


@admin.route('/acl/delete/<int:id>', methods=['GET'])
@admin_required
def acl_delete(id):
    acl = Acl.query.filter_by(id=id).first_or_404()
    acl.delete()
    flash(gettext('Acls of user {jmeno} deleted').format(jmeno=acl.user_name),'success')
    return redirect(url_for('.acl_list'))
