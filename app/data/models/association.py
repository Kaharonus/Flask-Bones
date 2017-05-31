#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..mixins import CRUDMixin
from .. import db


class U_G_Association(CRUDMixin, db.Model):
    __tablename__ = 'u-g_association'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship("User", back_populates="groups")
    groups = db.relationship("Group", back_populates="users")


class U_F_Association(CRUDMixin, db.Model):
    __tablename__ = 'u-f_association'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('firma.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship("User", back_populates="companies")
    companies = db.relationship("Company", back_populates="users")


class G_F_Association(CRUDMixin, db.Model):
    __tablename__ = 'g-f_association'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('firma.id'))
    groups = db.relationship("Group", backref=db.backref("groups_g", cascade="all, delete-orphan"))
    companies = db.relationship("Company", backref=db.backref("groups_f", cascade="all, delete-orphan"))