#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import (
    current_app, request, g, redirect, url_for, render_template, flash, abort
)
from flask_babel import gettext, lazy_gettext
from flask_login import login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeSerializer, BadSignature
from app.public.forms import RegisterGroupForm, RegisterCompanyForm, EditProfileForm
from app.extensions import lm
from app.data.models import User, Group, Company
from . import auth


@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash(gettext('You were logged out'), 'success')
    return redirect(url_for('public.login'))


@auth.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = RegisterGroupForm()
    if form.validate_on_submit():

        group = Group.create(name=form.data['name'],)

        flash(gettext('Group {name} created').format(name=group.name),'success')
        return redirect(url_for('admin.group_list'))
    return render_template('create_group.html', form=form)

@auth.route('/create_organization', methods=['GET', 'POST'])
@login_required
def create_organization():
    form = RegisterCompanyForm()
    if form.validate_on_submit():

        firma = Company.create(name=form.data['name'],
                             state=form.data['state'],
                             address=form.data['address'],
                             phone_number=form.data['phone_number'],
                             contact_person=form.data['contact_person'],
                             website=form.data['website'])

        flash(gettext('Organization {name} created').format(name=firma.name),'success')
        return redirect(url_for('admin.company_list'))
    return render_template('create_firma.html', form=form)


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        if User.if_exists_email(form.email._value()) and current_user.email!=form.email._value():
            flash(gettext("An account has already been registered with that email. Try another?"), 'warning')
            return render_template('profile-edit.html', form=form, user=current_user)
        if not current_user.username == form.username._value():
            flash(gettext("You little rebel! I like you!"), 'warning')
            return render_template('profile-edit.html', form=form, user=current_user)
        form.populate_obj(current_user)
        current_user.commit()
        flash(gettext('User {username} edited').format(username=current_user.username),'success')
    return render_template('profile-edit.html', form=form, user=current_user)
