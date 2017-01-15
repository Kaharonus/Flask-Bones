#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, g, current_app, jsonify
from flask_babel import lazy_gettext,gettext
from flask_login import login_required
from itsdangerous import URLSafeSerializer
from app.tasks import send_registration_email
from app.utils import admin_required
from app.data.models.acl import Acl
from app.data.models.ctecka import Ctecka
from app.data.models.firma import Firma
from app.public.forms import EditCteckaForm, CteckaForm, RegisterCteckaForm
from . import admin
from monsterurl import get_monster
import re



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
        sortable=[Ctecka.username],
        searchable=[Ctecka.username],
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
    acls = Acl.query.filter_by(ctecka_id=id).all()
    privateacls = Acl.query.filter_by(ctecka_id=id).filter(
        Acl.topic.ilike("/"+ctecka.monurl+"/%")).all()
    #for acl in acls:
    #    if "/"+ctecka.monurl+"/" in acl.topic
    #        privateacls
    form = EditCteckaForm(obj=ctecka)
    if form.validate_on_submit():
        if Ctecka.if_exists(form.username._value()) and ctecka.username != form.username._value():
            flash(gettext('Name already in use'), 'warning')
        else:
            if form.monurl.data == "":
                form.monurl.data = ctecka.monurl
            form.populate_obj(ctecka)
            ctecka.update()
            for acl in acls:
                acl.user_name = form.username.data
                acl.update()
            for privateacl in privateacls:
                privateacl.topic = re.sub(r"^/[^/]+/", "/"+form.monurl.data+"/", privateacl.topic, 1)
                acl.update()
            flash(gettext('Ctecka {nazev} edited').format(nazev=ctecka.username),'success')
    return render_template('ctecky-edit.html', form=form, ctecka=ctecka)


@admin.route('/ctecka/delete/<int:id>', methods=['GET'])
@admin_required
def ctecka_delete(id):
    ctecka = Ctecka.query.filter_by(id=id).first_or_404()
    ctecka.delete()
    flash(gettext('User {nazev} deleted').format(nazev=ctecka.username),'success')
    return redirect(url_for('.ctecka_list'))


@admin.route('/create_ctecka', methods=['GET', 'POST'])
def create_ctecka():
    form = RegisterCteckaForm()
    if form.validate_on_submit():
        ctecka = Ctecka.create(
            username=form.data['username'],
            firma_id=form.data['firma_id'],
            password=form.data['password'],
            monster=form.data['monster'],
            is_sadmin=form.data['is_sadmin']
        )
        flash(gettext('Organization {name} created').format(name=ctecka.username), 'success')
        return redirect(url_for('admin.ctecka_list'))
    return render_template('create_ctecka.html', form=form)


@admin.route('/ctecka/getmon', methods=['GET', 'POST'])
@admin_required
def get_mon():
    x = get_monster()
    while Ctecka.if_used(x):
        x = get_monster()
    return jsonify({"randvalue":x})