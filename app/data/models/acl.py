#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import db
from ..mixins import CRUDMixin


class Acl(CRUDMixin, db.Model):
    __tablename__ = "acl"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(128), nullable=False)
    rw = db.Column(db.Integer, nullable=False, default=0)
    user_name = db.Column(db.String(32), nullable=False)
    ctecka_id = db.Column(db.Integer, db.ForeignKey('ctecka.id'))
    ctecky = db.relationship("Ctecka", back_populates="acls")

    def __init__(self, topic, rw , ctecka, private):
        if private:
            self.topic = "/"+ctecka.monurl+topic
        else:
            self.topic = topic
        self.rw = rw
        self.user_name = ctecka.username
        self.ctecka_id = ctecka.id

    @staticmethod
    def if_exists(topic):
        if not Acl.query.filter_by(topic=topic).first():
            return False
        return True
