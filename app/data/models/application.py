from .. import db
from ..mixins import CRUDMixin
from itsdangerous import TimestampSigner
from flask import current_app
from .company import Company
import datetime

class Application(CRUDMixin, db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer, primary_key=True)
    application_name = db.Column(db.String(256))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    acl_net = db.Column(db.String(128), nullable=False)
    """(fe)"""
    email = db.Column(db.String(120), unique=True)
    __api_key = db.Column(db.String(512))

    def __init__(self, application_name, company_id, email, acl_net):
        self.application_name = application_name
        self.company_id = company_id
        self.acl_net = acl_net
        self.email = email
        self.__api_key = self.generate_api_key()

    def generate_api_key(self):
        hash = TimestampSigner(current_app.config['SECRET_KEY'])
        key = hash.sign(Company.find_by_id(self.company_id).company_name)
        return str(key, 'utf-8')

    @staticmethod
    def get_api_key(id):
        # returns hashed api_key
        return db.session.query(Application).filter_by(id=id).first().__api_key

    @staticmethod
    def validate_api_key(id, api_key):
        hashed_api_key = Application.get_api_key(id)
        # if Company.query.filter_by(api_key=api_key).first() is None:
        if hashed_api_key is None:
            return True
        elif not Bcrypt.check_password_hash(hashed_api_key, api_key):
            return True
        else:
            return False