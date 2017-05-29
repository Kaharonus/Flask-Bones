#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import db
from ..mixins import CRUDMixin
import datetime
from .association import G_F_Association
from .company import Company
from .association import U_G_Association


class Group(CRUDMixin, db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(128), nullable=False, unique=True)
    created_ts = db.Column(db.DateTime(), nullable=False)
    users = db.relationship("U_G_Association", back_populates="groups")
    companies = db.relationship("G_F_Association", cascade="all, delete-orphan")
    # TODO: Establish which users are admins

    def __init__(self, nazev):
        self.group_name = nazev
        self.created_ts = datetime.datetime.now()

    def __repr__(self):
        return '<Group %s>' % self.group_name

    def to_json(self):
        return [self.group_name]

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
    def if_exists(group, company_id):

        item = db.session.query(Group)\
                         .join(G_F_Association)\
                         .join(Company)\
                         .filter(Group.name == group and Company.id == company_id)\
                         .first()
        return True if item else False
