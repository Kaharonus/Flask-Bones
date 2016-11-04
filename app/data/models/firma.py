#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import db
from ..mixins import CRUDMixin
import datetime

class Firma(CRUDMixin, db.Model):
    __tablename__ = "firma"

    id = db.Column(db.Integer, primary_key=True)
    nazev = db.Column(db.String(128), nullable=False, unique=True)
    created_ts = db.Column(db.DateTime(), nullable=False)
    users = db.relationship("U_F_Association", back_populates="firmy")
    groups = db.relationship("G_F_Association", back_populates="firmy")

    state = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    contact_person = db.Column(db.String(64))
    phone_number = db.Column(db.String(16), nullable=False)
    website = db.Column(db.String(64))

    def __init__(self, nazev, state, address, phone_number, contact_person=None, website=None):
        self.nazev = nazev
        self.state = state
        self.address = address
        self.phone_number = phone_number
        self.contact_person = contact_person
        self.website = website
        self.created_ts = datetime.datetime.now()

    def __repr__(self):
        return '<Firma %s>' % self.nazev

    @staticmethod
    def find_by_id(id):
        return db.session.query(Firma.id, Firma.nazev).filter_by(id=id).first()