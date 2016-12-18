#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import db
from ..mixins import CRUDMixin
from flask_login import UserMixin
from app.data import hashing_passwords as h_p


class Acl_User(CRUDMixin, UserMixin, db.Model):
    __tablename__ = "acl_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    auth_hash = db.Column(db.String(256), nullable=False)
    active = db.Column(db.Boolean())
    is_sadmin = db.Column(db.Boolean())
    firma_id = db.Column(db.Integer, db.ForeignKey('firma.id'), nullable=False)
    acls = db.relationship("Acl", cascade = "all, delete-orphan")

    def __init__(self, username, email, jmeno, prijmeni, password, active=False, is_sadmin=False):
        self.username = username
        self.email = email
        self.set_password(password)
        self.active = active
        self.is_sadmin = is_sadmin

    def __repr__(self):
        return '<User %s>' % self.username

    def set_password(self, password):
        self.auth_hash = h_p.make_hash(password)

    def check_password(self, password):
        return h_p.check_hash(self.auth_hash, password.encode('utf-8'))


    def to_json(self):
        return [self.username]

    # @classmethod
    # def stats(cls):
    #     active_users = cache.get('active_users')
    #     if not active_users:
    #         active_users = cls.query.filter_by(active=True).count()
    #         cache.set('active_users', active_users)
    #
    #     inactive_users = cache.get('inactive_users')
    #     if not inactive_users:
    #         inactive_users = cls.query.filter_by(active=False).count()
    #         cache.set('inactive_users', inactive_users)
    #
    #     return {
    #         'all': active_users + inactive_users,
    #         'active': active_users,
    #         'inactive': inactive_users
    #     }
    #
    @staticmethod
    def if_exists(username):
        if not Acl_User.query.filter_by(username=username).first():
            return False
        return True