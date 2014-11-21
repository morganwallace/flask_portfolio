from flask import Flask
from flask import render_template
from flask import session, request, make_response, jsonify, flash, url_for, redirect,g
from flask.ext.sqlalchemy import SQLAlchemy
# from functools import wraps
# from flask.ext.login import login_user, LoginManager, logout_user, current_user, login_required
# from flask.ext.openid import OpenID
import os,time
from datetime import date

app = Flask(__name__)


# Loads configuration from `config.py`
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')

####### Database classes/schema
from manage import db, Project


@app.route('/')
def home():
    projects=db.session.query(Project.title,Project.body,Project.projectType,Project.tags,Project.externalLink,Project.imagesLinks,Project.snippet,Project.date).all()
    # all_users = User.query.all()
    projectsList=[]

    for proj in projects:
        app.logger.debug(proj[5].split(",")[0])
        projectsList.append({
            'title':str(proj[0]).title(),
            'body':proj[1],
            'projectType':proj[2],
            'tags':proj[3].split(","),
            'externalLink':proj[4],
            'imagesLinks':url_for('static',filename='img/'+proj[5].split(",")[0]), #only take first photo
            'snippet':proj[6],
            'date':date.fromtimestamp(proj[7]*24*3600).strftime("%d %b %Y"),
            'timestamp':proj[7],
            })
    projectsList= sorted(projectsList, key=lambda k: k['timestamp'])
    projectsList.reverse()

    gaID=os.environ.get('gaID')
    return render_template('index.html',
        projectsList=projectsList,gaID=gaID)


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
    title=title.replace("-"," ")
    myproject=db.session.query(Project.title,Project.body,Project.projectType,Project.tags,Project.externalLink,Project.imagesLinks,Project.date).filter(Project.title==title.lower()).first()
    app.logger.debug(myproject)
    app.logger.debug(title)
    title=str(myproject[0]).title()
    app.logger.debug(myproject[5].split(","))
    return render_template('project.html',
        title=title, 
        body=myproject[1],
        projectType=myproject[2],
        tags=myproject[3].split(","),
        externalLink=myproject[4],
        imagesLinks=myproject[5].split(",")[1:],
        pageTitle=title+" - Morgan Wallace",
        date=date.fromtimestamp(myproject[6]*24*3600).strftime("%b %d, %Y"),
        coverphoto=myproject[5].split(",")[0],
        )   


@app.route('/tags/<tag>')
def tag(tag):
    projects=db.session.query(Project.title,Project.body,Project.projectType,Project.tags,Project.externalLink,Project.imagesLinks,Project.snippet,Project.date).filter(Project.tags.contains(tag)).all()
    # projects=db.session.query(Project.title,Project.body,Project.projectType,Project.tags,Project.externalLink,Project.imagesLinks).filter(.all()    
    projectsList=[]

    for proj in projects:
        # app.logger.debug(proj[7])
        projectsList.append({
            'title':str(proj[0]).title(),
            'body':proj[1],
            'projectType':proj[2],
            'tags':proj[3].split(","),
            'externalLink':proj[4],
            'imagesLinks':url_for('static',filename='img/'+proj[5].split()[0]), #only take first photo
            'snippet':proj[6],
            'date':date.fromtimestamp(proj[7]*24*3600).strftime("%d %b %Y"),
            'timestamp':proj[7],
            })
    return render_template('tags.html', projectsList=projectsList,pageTitle=tag+" - Morgan Wallace")   


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

    #to run a debug mode only when developing locally run this in terminal:
    # $ export SERVERTYPE="dev"
    # print os.environ.get('SERVERTYPE')
    if os.environ.get('SERVERTYPE')=='dev':
        app.debug = True
        # print 'debug mode'

    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)