from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ayzcctpvbmwajn:z1bTq5u6fbqWmGFHR0UrOpN_zW@ec2-54-197-249-167.compute-1.amazonaws.com:5432/d25indqqmd1654"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    picture_url=db.Column(db.String(120))
    username=db.Column(db.String(80))
    password=db.Column(db.String(80))

    def __init__(self, firstname, lastname, email, username,password,picture_url=None):
        self.firstname = firstname
        self.lastname = firstname
        self.email = email
        # self.my_id=my_id
        self.picture_url=picture_url
        self.username=username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


    def __repr__(self):
        return '<ROW with label: User ID %r>' % self.id


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    user_id =db.Column(db.Integer)
    projectType=db.Column(db.String(255))
    tags=db.Column(db.String(255))
    externalLink=db.Column(db.String(255))
    imagesLinks=db.Column(db.String(255))
    snippet=db.Column(db.String(255))
    date=db.Column(db.Integer)


    def __init__(self, title, body,user_id,projectType,tags,externalLink,imagesLinks,snippet,date):
        self.title = title
        self.body = body
        self.user_id= user_id
        self.project_type=projectType
        self.tags=tags
        self.externalLink=externalLink
        self.imagesLinks=imagesLinks
        self.snippet=snippet
        self.date=date

    def __repr__(self):
        return '<ROW with label: project ID %r>' % self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer)
    project_id = db.Column(db.Integer)
    body = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


    def __init__(self, user_id, project_id,body):
        self.user_id=user_id
        self.project_id=project_id
        self.body=body

    def __repr__(self):
        return '<ROW with label: Comment ID %r>' % self.id

if __name__ == '__main__':
    manager.run()