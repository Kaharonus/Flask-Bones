from flask_login import UserMixin
from app.extensions import cache, bcrypt
from itsdangerous import TimestampSigner, SignatureExpired
import bcrypt as bcr
from flask import current_app
from .. import db
from ..mixins import CRUDMixin
import datetime
from . import Group
import time

class User(CRUDMixin, UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=True, unique=True)
    jmeno = db.Column(db.String(128), nullable=True)
    prijmeni = db.Column(db.String(128), nullable=True)
    pw_hash = db.Column(db.String(256), nullable=True)
    created_ts = db.Column(db.DateTime(), nullable=False)
    remote_addr = db.Column(db.String(20))
    active = db.Column(db.Boolean())
    is_sadmin = db.Column(db.Boolean())
    default_idfirm = db.Column(db.Integer, nullable=True)
    api_key = db.Column(db.String(512), nullable=True)
    oauth = db.relationship('Oauth', backref='user',
                            lazy='dynamic')
    #id = db.Column(db.Integer, primary_key=True)
    #social_id = db.Column(db.String(64), nullable=False, unique=True) -> username
    #nickname = db.Column(db.String(64), nullable=True) -> jmeno
    #email = db.Column(db.String(64), nullable=True)
    groups = db.relationship("U_G_Association", back_populates="users")
    firmy = db.relationship("U_F_Association", back_populates="users")

    def __init__(self, username, email, jmeno, prijmeni, password, remote_addr, active=False, is_sadmin=False):
        self.username = username
        self.email = email
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.set_password(password)
        self.created_ts = datetime.datetime.now()
        self.remote_addr = remote_addr
        self.active = active
        self.is_sadmin = is_sadmin
        self.api_key = self.generate_auth_token()

    def __repr__(self):
        return '<User (username=%s, first_name=%s, last_name=%s, api_key=%s)>' % (self.username, self.jmeno, self.prijmeni, self.api_key)

    def set_password(self, password):
        self.pw_hash = bcrypt.generate_password_hash(password, 10)
        #pwhash = bcr.hashpw(password.encode('utf-8'), bcr.gensalt())
        #self.pw_hash = pwhash.decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password.encode('utf-8'))

    def generate_auth_token(self, expiration = 20):#config['AUTH_TOKEN_EXPIRATION']):
        s = TimestampSigner(current_app.config['SECRET_KEY'])
        key = s.sign(self.username)
        return str(key,'utf-8')

    def to_json(self):
        return [self.id, self.jmeno + ' ' + self.prijmeni + ' (' + self.username + ')']

    @classmethod
    def stats(cls):
        active_users = cache.get('active_users')
        if not active_users:
            active_users = cls.query.filter_by(active=True).count()
            cache.set('active_users', active_users)

        inactive_users = cache.get('inactive_users')
        if not inactive_users:
            inactive_users = cls.query.filter_by(active=False).count()
            cache.set('inactive_users', inactive_users)

        return {
            'all': active_users + inactive_users,
            'active': active_users,
            'inactive': inactive_users
        }

    @staticmethod
    def if_exists(username):
        if not User.query.filter_by(username=username).first():
            return False
        return True


    @staticmethod
    def if_exists_email(email):
        if not User.query.filter_by(email=email).first():
            return False
        return True

    @staticmethod
    def find_by_name(name):
        return User.query.filter_by(jmeno=name).first()

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_in_group(group_id):
        from . import U_G_Association
        return User.query.join(U_G_Association).join(Group).filter(Group.id==group_id).all()

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user
