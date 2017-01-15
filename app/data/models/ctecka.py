#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import db
from ..mixins import CRUDMixin
from flask_login import UserMixin
from app.data import hashing_passwords as h_p
from monsterurl import get_monster
import random
import string


class Ctecka(CRUDMixin, UserMixin, db.Model):
    __tablename__ = "ctecka"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    auth_hash = db.Column(db.String(256), nullable=False)
    firma_id = db.Column(db.Integer, db.ForeignKey('firma.id'), nullable=False)
    acls = db.relationship("Acl", cascade="all, delete-orphan")
    firmy = db.relationship("Firma", back_populates="ctecky")
    is_sadmin = db.Column(db.Boolean())
    monurl = db.Column(db.String(64), nullable=False)

    def __init__(self, username, firma_id, password, is_sadmin, monster):
        self.username = username
        self.firma_id = firma_id.id
        self.set_password(password)
        self.is_sadmin = is_sadmin
        if monster:
            self.monurl = get_monster()
            while Ctecka.if_used(self.monurl):
                self.monurl = get_monster()
        else:
            self.monurl = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64))
            while Ctecka.if_used(self.monurl):
                self.monurl = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64))

    @staticmethod
    def if_exists(username):
        if not Ctecka.query.filter_by(username=username).first():
            return False
        return True

    @staticmethod
    def if_used(monurl):
        if not Ctecka.query.filter_by(monurl=monurl).first():
            return False
        return True

    @staticmethod
    def find_by_id(id):
        return db.session.query(Ctecka).filter_by(id=id).first()

    def __repr__(self):
        return '%s' % self.username

    def set_password(self, password):
        self.auth_hash = h_p.make_hash(password)

    def check_password(self, password):
        return h_p.check_hash(password.encode('utf-8'), self.auth_hash)

    def to_json(self):
        return [self.username]
