#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, g, current_app
from flask_babel import lazy_gettext,gettext
from flask_login import login_required
from itsdangerous import URLSafeSerializer
from app.tasks import send_registration_email
from app.utils import admin_required
from app.data.models.ctecka import Ctecka
from app.data.models.firma import Firma
from app.public.forms import EditCteckaForm, CteckaForm
from . import admin


@admin.route('/ctecka/list', methods=['GET', 'POST'])
@login_required
def ctecka_list():
    if Ctecka.query.all() == []:
        firma_nazev = ""
    else:
        firma_nazev = Firma.find_by_id(Ctecka.firma_id).nazev
    from app.data import DataTable
    datatable = DataTable(
        model=Ctecka,
        columns=[],
        sortable=[Ctecka.nazev],
        searchable=[Ctecka.nazev],
        filterable=[],
        limits=[10, 25, 50, 100],
        request=request
    )

    if g.pjax:
        return render_template(
            'ctecky.html',
            firma_nazev = firma_nazev,
            datatable=datatable
        )

    return render_template(
        'ctecky-list.html',
        firma_nazev = firma_nazev,
        datatable=datatable
    )


@admin.route('/ctecka/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def ctecka_edit(id):
    ctecka = Ctecka.query.filter_by(id=id).first_or_404()
    form = EditCteckaForm(obj=ctecka)
    if form.validate_on_submit():
        form.populate_obj(ctecka)
        ctecka.update()
        flash(gettext('Ctecka {nazev} edited').format(nazev=ctecka.nazev),'success')
    return render_template('ctecky-edit.html', form=form, ctecka=ctecka)


@admin.route('/ctecka/delete/<int:id>', methods=['GET'])
@admin_required
def ctecka_delete(id):
    ctecka = Ctecka.query.filter_by(id=id).first_or_404()
    ctecka.delete()
    flash(gettext('User {nazev} deleted').format(nazev=ctecka.nazev),'success')
    return redirect(url_for('.ctecka_list'))


@admin.route('/create_ctecka', methods=['GET', 'POST'])
def create_ctecka():
    form = CteckaForm()
    if form.validate_on_submit():
        Ctecka.create(
            nazev=form.data['nazev'],
            firma_id=form.data['firma_id']
        )
        return redirect(url_for('public.index'))
    return render_template('create_ctecka.html', form=form)