from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import datetime

app = Flask(__name__)

# Don't store the DB URI in Source Code. 
# Set it as environmental variable and fetch it here

# Loads configuration from `config.py`
from config import *
# Use production database (uncomment for override)
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    user_id =db.Column(db.Integer)
    projectType=db.Column(db.String(255))
    tags=db.Column(db.String(255))
    externalLink=db.Column(db.String(255))
    imagesLinks=db.Column(db.String(255))
    snippet=db.Column(db.String(255))
    codeLink=db.Column(db.String(255))
    cover_photo=db.Column(db.String(255))
    thumbnail=db.Column(db.String(255))
    date=db.Column(db.DateTime)
    # user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self, title, body,user_id,projectType,tags,externalLink,imagesLinks,snippet,codeLink,cover_photo,thumbnail,date):
        self.title = title
        self.body = body
        self.user_id= user_id
        self.project_type=projectType
        self.tags=tags
        self.externalLink=externalLink
        self.imagesLinks=imagesLinks
        self.snippet=snippet
        self.codeLink=codeLink
        self.cover_photo=cover_photo
        self.thumbnail=thumbnail
        self.date=date
        
    def __repr__(self):
        return '<ROW with label: project ID %r>' % self.id


# Create user model.
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)
    # projects = db.relationship("project")

    def __init__(self , username ,password , email,firstname,lastname):
        self.firstname=firstname
        self.lastname=lastname
        self.username=username
        self.password=self.set_password(password) 
        self.email=email
        self.registered_on = datetime.utcnow()  

    ### secure passwords    
    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password) 


    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


if __name__ == '__main__':
    manager.run()