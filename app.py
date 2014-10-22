from flask import Flask
from flask import render_template
from flask import session, request, make_response, jsonify, flash, url_for, redirect,g
from flask.ext.sqlalchemy import SQLAlchemy
# from functools import wraps
# from flask.ext.login import login_user, LoginManager, logout_user, current_user, login_required
# from flask.ext.openid import OpenID
import os,time

app = Flask(__name__)


# Loads configuration from `config.py`
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ayzcctpvbmwajn:z1bTq5u6fbqWmGFHR0UrOpN_zW@ec2-54-197-249-167.compute-1.amazonaws.com:5432/d25indqqmd1654"

####### Database classes/schema
from manage import db, User, Project


@app.route('/')
def home():
    projects=db.session.query(Project.title,Project.body,Project.projectType,Project.tags,Project.externalLink,Project.imagesLinks,Project.snippet).all()
    # all_users = User.query.all()
    projectsList=[]
    for proj in projects:
        projectsList.append({
            'title':str(proj[0]).title(),
            'body':proj[1],
            'projectType':proj[2],
            'tags':proj[3],
            'externalLink':proj[4],
            'imagesLinks':proj[5].split()[0], #only take first photo
            'snippet':proj[6],
            })
    return render_template('index.html',
        projectsList=projectsList)


@app.route('/add')
# @login_required
def add():
    return render_template('add.html')

@app.route('/addproject' , methods=['POST'])
def add_project():
    app.logger.debug("/addproject in app.py:\n"+str(request.form))
    user_id = request.cookies.get('user_id')
    # app.logger.debug(user_id)
    #args to init a project: title, body,user_id,project_type,tags
    #add to database
    project= Project(
        title=request.form['title'].lower(), #lower cased to ensure proper url formatting
        body=request.form['body'],
        user_id=user_id,
        projectType=request.form['projectType'],
        tags=request.form['tags'],
        externalLink=request.form['externalLink'],
        imagesLinks=request.form['imagesLinks'],
        snippet=request.form['snippet'],
        date=int(time.mktime(time.strptime(request.form['date'],"%m/%d/%Y")))/3600/24,
        )
    # time.strptime(request.form['date'],"%m/%d/%Y")
    db.session.add(project)
    db.session.commit()
    app.logger.debug("Successfully project added to database")
    resp = make_response(jsonify(success=True,title=request.form['title']))
    return resp



@app.route('/project/<title>')
def project(title):
    myproject=db.session.query(Project.title,Project.body,Project.projectType,Project.tags,Project.externalLink,Project.imagesLinks).filter(Project.title==title.lower()).first()
    title=str(myproject[0]).title()
    # app.logger.debug('opening /project/'+title+'\n'+project.all())
    return render_template('project.html',
        title=title, 
        body=myproject[1],
        projectType=myproject[2],
        tags=myproject[3].split(","),
        externalLink=myproject[4],
        imagesLinks=myproject[5].split(","),
        pageTitle=title+" - Morgan Wallace")   





@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404




if __name__ == '__main__':
    # app.run()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    # app.run(debug=True)

