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




if __name__ == '__main__':
    manager.run()