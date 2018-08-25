from flask import Flask, g
from .ext import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean,Text
from flask_login import UserMixin
from blog.utils import login_manager
from config import SECRET_KEY
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """Represents Proected users."""

    # Set the name for table
    __tablename__ = 'user'
    id = Column(String(64), primary_key=True)
    username = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    email = Column(String(255), unique=True)

    # role_id = Column(Integer, ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute/ password 不是一个可读属性。')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        # user = User.query.filter_by(username = username).first()
        # if not user or not user.verify_password(password):
        #     return False
        # g.user = user
        # return True

    def generate_auth_token(self, expiration=600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        data = s.dumps({'id': self.id})
        print(data)
        return data

    @staticmethod
    def verify_auth_token(token, expiration=600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class Article(db.Model):
    """文章"""
    __tablename__ = 'Article'
    id = Column(Integer(), primary_key=True)
    author = Column(String(64))
    title = Column(String(256))
    brief = Column(String(256))
    content = Column(Text())
    status =Column(Integer(),default='0')
    create_date = Column(DateTime)
    published_date = Column(DateTime)
    approved = Column(Boolean, default=False)


class Category(db.Model):
    """版块"""
    __tablename__ = 'Category'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
class Tag(db.Model):
    """标签"""
    __tablename__ = 'Tag'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))


