#encoding: utf-8
from werkzeug.security import  generate_password_hash, check_password_hash
from exts import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serilalizer
from flask_login import UserMixin
from datetime import datetime
'''from flask_googlelogin import GoogleLogin
googlelogin = GoogleLogin(app)'''

class User(UserMixin,db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String(50),nullable=False)
    username=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    post = db.relationship('Post',backref='author',lazy='dynamic')

    def generate_confirmation_token(self,expiration=7200):
        s =Serilalizer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    #check password
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

class Post(db.Model):
    __tablename__= 'post'
    id = db.Column(db.Integer, primary_key=True)
    postname = db.Column(db.String(50), nullable = False)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    comment = db.Column(db.Text,nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    auhtor_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    post = db.relationship('Post', backref=db.backref('comments'))
    author = db.relationship('User',backref=db.backref('comments'))
