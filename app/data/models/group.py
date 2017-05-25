#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import db
from ..mixins import CRUDMixin
import datetime
from .association import G_F_Association
from .firma import Firma
from .association import U_G_Association

class Group(CRUDMixin, db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    nazev = db.Column(db.String(128), nullable=False, unique=True)
    created_ts = db.Column(db.DateTime(), nullable=False)
    users = db.relationship("U_G_Association", back_populates="groups")
    companies = db.relationship("G_F_Association", cascade="all, delete-orphan")
    # TODO: Establish which users are admins

    def __init__(self, nazev):
        self.nazev = nazev
        self.created_ts = datetime.datetime.now()

    def __repr__(self):
        return '<Group %s>' % self.nazev

    def to_json(self):
        return [self.nazev]

    def add_user(self, user):
        assoc = U_G_Association()
        assoc.group_id = self.id
        assoc.user_id = user.id
        assoc.save()

    def remove_user(self, user):
        assoc = U_G_Association.query.filter_by(group_id=self.id, user_id=user.id).first()
        if assoc:
            return assoc.delete()
        return False

    @staticmethod
    def if_exists(group, idfirm):
        if not db.session.query(Group).join(G_F_Association).join(Firma).filter(Group.name == group and Firma.id == idfirm).first():
            return False
        return True