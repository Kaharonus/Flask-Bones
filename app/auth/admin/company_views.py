#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, g
from flask_babel import lazy_gettext,gettext
from flask_login import login_required

from app.utils import admin_required, crypt
from app.data.models import Company
from app.public.forms import EditCompanyForm
from . import admin


@admin.route('/firma/list', methods=['GET', 'POST'])
@admin_required
def company_list():

    from app.data import DataTable

    datatable = DataTable(
        model=Company,
        columns=[],
        sortable=[Company.company_name, Company.created_ts],
        searchable=[Company.company_name],
        filterable=[],
        limits=[25, 50, 100],
        request=request
    )

    if g.pjax:
        return render_template(
            'company.html',
            datatable=datatable
        )

    return render_template(
        'company-list.html',
        datatable=datatable
    )


@admin.route('/firma/edit/<str_hash>', methods=['GET', 'POST'])
@admin_required
def company_edit(str_hash):

    id = int(float(crypt(str_hash, decrypt=True)))
    company = Company.query.filter_by(id=id).first_or_404()
    form = EditCompanyForm(obj=company)

    if form.validate_on_submit():
        form.populate_obj(company)
        company.commit()
        flash(gettext('Organization {company_name} edited').format(company_name=company.company_name), 'success')

    return render_template('company-edit.html', form=form, firma=company)


@admin.route('/firma/delete/<str_hash>', methods=['GET'])
@admin_required
def company_delete(str_hash):

    id = int(float(crypt(str_hash, decrypt=True)))
    company = Company.query.filter_by(id=id).first_or_404()
    company.delete()
    flash(gettext('Organization {name} deleted').format(name=company.company_name), 'success')

    return redirect(url_for('.company_list'))
