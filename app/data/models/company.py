#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import db
from ..mixins import CRUDMixin
from itsdangerous import TimestampSigner
from flask import current_app
import datetime
from flask_bcrypt import Bcrypt
from .association import G_F_Association, U_F_Association


class Company(CRUDMixin, db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(128), nullable=False, unique=True)
    created_ts = db.Column(db.DateTime(), nullable=False)
    users = db.relationship("U_F_Association", back_populates="companies")
    groups = db.relationship("G_F_Association", cascade="all, delete-orphan")

    state = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    contact_person = db.Column(db.String(64))
    phone_number = db.Column(db.String(16), nullable=False)
    website = db.Column(db.String(64))


    def __init__(self, company_name, state, address, phone_number, contact_person=None, website=None):
        self.company_name = company_name
        self.state = state
        self.address = address
        self.phone_number = phone_number
        self.contact_person = contact_person
        self.website = website
        self.created_ts = datetime.datetime.now()
        #self.api_key = self.generate_api_key()

    def __repr__(self):
        return '<Company %s>' % self.name

    def add_group(self, group):
        assoc = G_F_Association()
        assoc.company_id = self.id
        assoc.group_id = group.id
        assoc.save()

    def add_user(self, user):
        assoc = U_F_Association()
        assoc.company_id = self.id
        assoc.user_id = user.id
        assoc.save()


    @staticmethod
    def find_by_id(searched_id):
        return db.session.query(Company).filter_by(id=searched_id).first()

