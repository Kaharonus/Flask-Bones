from flask.ext.login import UserMixin
from app.extensions import cache ,bcrypt
import bcrypt as bcr
from .. import db
from ..mixins import CRUDMixin
import datetime



class User(CRUDMixin, UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    jmeno = db.Column(db.String(64), nullable=False )
    prijmeni = db.Column(db.String(64), nullable=False)
    pw_hash = db.Column(db.String(256), nullable=False)
    created_ts = db.Column(db.DateTime(), nullable=False)
    remote_addr = db.Column(db.String(20))
    active = db.Column(db.Boolean())
    is_admin = db.Column(db.Boolean())
    default_idfirm = db.Column(db.Integer, nullable=True)
    groups = db.relationship("U_G_Association", back_populates="users")
    firmy = db.relationship("U_F_Association", back_populates="users")

    def __init__(self, username, email, jmeno, prijmeni, password, remote_addr, active=False, is_admin=False):
        self.username = username
        self.email = email
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.set_password(password)
        self.created_ts = datetime.datetime.now()
        self.remote_addr = remote_addr
        self.active = active
        self.is_admin = is_admin

    def __repr__(self):
        return '<User %s>' % self.username

    def set_password(self, password):
        #self.pw_hash = bcrypt.generate_password_hash(password, 10)
        pwhash = bcr.hashpw(password.encode('utf-8'), bcr.gensalt())
        self.pw_hash = pwhash.decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password.encode('utf-8'))

    def to_json(self):
        return [self.username]

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
    def if_exists(username):
        if not User.query.filter_by(username=username).first():
            return False
        return True
