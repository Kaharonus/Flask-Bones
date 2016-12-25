#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import db
from ..mixins import CRUDMixin


class Acl(CRUDMixin, db.Model):
    __tablename__ = "acl"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(128), nullable=False)
    rw = db.Column(db.Integer, nullable=False, default=0)
    user_name = db.Column(db.String(32), db.ForeignKey('acl_user.username'), nullable=False)
    ctecka_id = db.Column(db.Integer, db.ForeignKey('ctecka.id'))
    ctecky = db.relationship("Ctecka", back_populates="acls")

    def __init__(self, topic, user_name, rw , ctecka_id):
        self.topic = "/{}/{}/{}".format(ctecka_id.nazev, user_name, topic)
        self.rw = int(rw)
        #self.rw = rw
        self.user_name = user_name
        self.ctecka_id = ctecka_id

    @staticmethod
    def if_exists(topic, user_name):
        if not Acl.query.filter_by(topic=topic, user_name=user_name).first():
            return False
        return True