#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..mixins import CRUDMixin
from .. import db

class U_G_Association(CRUDMixin, db.Model):
    __tablename__ = 'u-g_association'
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    users = db.relationship("User", back_populates="groups")
    groups = db.relationship("Group", back_populates="users")

class U_F_Association(CRUDMixin, db.Model):
    __tablename__ = 'u-f_association'
    firma_id = db.Column(db.Integer, db.ForeignKey('firma.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    users = db.relationship("User", back_populates="firmy")
    firmy = db.relationship("Firma", back_populates="users")

class G_F_Association(CRUDMixin, db.Model):
    __tablename__ = 'g-f_association'
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    firma_id = db.Column(db.Integer, db.ForeignKey('firma.id'), primary_key=True)
    groups = db.relationship("Group", back_populates="firmy")
    firmy = db.relationship("Firma", back_populates="groups")