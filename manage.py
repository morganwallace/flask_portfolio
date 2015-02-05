from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


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
    codeLink=db.Column(db.String(255))
    cover_photo=db.Column(db.String(255))
    

    def __init__(self, title, body,user_id,projectType,tags,externalLink,imagesLinks,snippet,date,codeLink,cover_photo):
        self.title = title
        self.body = body
        self.user_id= user_id
        self.project_type=projectType
        self.tags=tags
        self.externalLink=externalLink
        self.imagesLinks=imagesLinks
        self.snippet=snippet
        self.date=date
        self.codeLink=codeLink
        self.cover_photo=cover_photo
        
    def __repr__(self):
        return '<ROW with label: project ID %r>' % self.id


# Create user model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)

    def __init__():
        self.first_name=first_name
        self.last_name=last_name
        self.login=login
        self.username=username
        self.password=password
        self.email=email
        self.registered_on = datetime.utcnow()        

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