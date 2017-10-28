#encoding:utf-8
import os
DEBUG = True
SECRET_KEY = os.urandom(24)

HOSTNAME ='127.0.0.1'
PORT = '3306'
DATABASE =  'flask_DB'
USERNAME = 'root'
PASSWORD = '1234'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False
'''
class Auth:
    CLIENT_ID = ('922468949333-u5t6edqk3e2ftjqe2o08eqi1miik53u8.apps.googleusercontent.com')
    CLIENT_SECRET = 'W1aMQ6AmdDnp5ZI4P-JWPQ5F'
    REDIRECT_URI = 'http://localhost:5000/login.html'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
'''
