#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import db
from ..mixins import CRUDMixin


class Ctecka(CRUDMixin, db.Model):
    __tablename__ = "ctecka"

    id = db.Column(db.Integer, primary_key=True)
    nazev = db.Column(db.String(32), nullable=False)
    firma_id = db.Column(db.Integer, db.ForeignKey('firma.id'), nullable=False)
    acls = db.relationship("Acl", cascade="all, delete-orphan")
    firmy = db.relationship("Firma", back_populates="ctecky")

    def __init__(self, nazev, firma_id):
        self.nazev = nazev
        self.firma_id = firma_id.id

    @staticmethod
    def if_exists(nazev):
        if not Ctecka.query.filter_by(nazev=nazev).first():
            return False
        return True

    @staticmethod
    def find_by_id(id):
        return db.session.query(Ctecka).filter_by(id=id).first()