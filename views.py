from flask import session, request, make_response, jsonify, flash, url_for, redirect,g,render_template,Flask, abort ,g
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import jinja2

import markdown
from flask import Markup

import os,time
from datetime import date
import datetime

from app import app
from manage import db, Project, User

# Loads configuration from `config.py`
# from config import *
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# ### O auth for Twitter
# from flask_oauth import OAuth
# oauth = OAuth()
# twitter = oauth.remote_app('twitter',
#     base_url='https://api.twitter.com/1/',
#     request_token_url='https://api.twitter.com/oauth/request_token',
#     access_token_url='https://api.twitter.com/oauth/access_token',
#     authorize_url='https://api.twitter.com/oauth/authenticate',
#     consumer_key='NUNxNmIWQpPQpWySkQAXKol4A',
#     consumer_secret='WXQFOsJf6DXEvWsdMqQNXOSirfI5ZXLFXtaJ2hQvQ3fUgdPbSZ'
# )
# @twitter.tokengetter
# def get_twitter_token(token=None):
#     return session.get('twitter_token')

# @app.route('/logintwitter')
# def logintwitter():
#     return twitter.authorize(callback=url_for('oauth_authorized',
#         next=request.args.get('next') or request.referrer or None))

# @app.route('/oauth-authorized')
# @twitter.authorized_handler
# def oauth_authorized(resp):
#     next_url = request.args.get('next') or url_for('home')
#     app.logger.debug(resp)
#     if resp is None:
#         flash(u'You denied the request to sign in.')
#         return redirect(next_url)

#     session['twitter_token'] = (
#         resp['oauth_token'],
#         resp['oauth_token_secret']
#     )
#     session['twitter_user'] = resp['screen_name']

#     flash('You were signed in as %s' % resp['screen_name'])
#     return redirect(next_url)

### End O Auth

from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from werkzeug.security import check_password_hash

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




# login setup from tutorial: 
# https://blog.openshift.com/use-flask-login-to-add-user-authentication-to-your-python-application/
@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html',pageTitle='register')
    user = User(request.form['username'] , request.form['password'],request.form['email'],request.form['firstname'] ,request.form['lastname'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))
 
 
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None or check_password_hash(registered_user.password,password) is False:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user, remember = remember_me)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('home')) 

@app.before_request
def before_request():
    g.user = current_user

### End Login views



def get_first_image(img_str):
    app.logger.debug(img_str)
    try:
        img_url=url_for('static',filename='img/'+img_str.split(",")[0])
    except:
        return None
    return img_url


@app.route('/')
def home():
    projects=Project.query.order_by(desc(Project.date)).all()
    
    # all_users = User.query.all()
    # projectsList=[]
    # img_url=get_first_image(proj[5])
    # for proj in projects:
        
    #     projectsList.append({
    #         'title':str(proj[0]).title(),
    #         'body':Markup(markdown.markdown(proj[1])),
    #         'projectType':proj[2],
    #         'tags':proj[3].split(","),
    #         'externalLink':proj[4],
    #         'imagesLinks':get_first_image(proj[5]), #only take first photo
    #         'snippet':proj[6],
    #         'date':date.fromtimestamp(proj[7]*24*3600).strftime("%b %Y"),
    #         'timestamp':proj[7],
    #         })
    # projects=[project.__dict__ for project in projects]
    # projects= sorted(projects, key=lambda k: k['date'])
    # projects.reverse()

    
    return render_template('index.html',
        projectsList=projects)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/add')
@login_required
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
        cover_photo=request.form['coverphoto'],
        codeLink=request.form['codelink']
        )
    # time.strptime(request.form['date'],"%m/%d/%Y")
    db.session.add(project)
    db.session.commit()
    app.logger.debug("Successfully project added to database")
    resp = make_response(jsonify(success=True,title=request.form['title']))
    return resp

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ravelry')
def ravelry():
    return render_template('ravelry.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/project/<title>')
def project(title):
    title=title.replace("-"," ")
    myproject=Project.query.filter(Project.title==title.lower()).first()
    myproject.title=str(myproject.title).title()

    return render_template("project.html",project=myproject)

@app.route('/tags/<tag>')
def tag(tag):
    projects=Project.query.filter(Project.tags.contains(tag)).all()
   
    return render_template('tags.html', projectsList=projects,pageTitle=tag+" - Morgan Wallace",tag=tag)   


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


def addtagfx(mylist, tag):
    '''convenience function to '''
    l=mylist.split("\n")
    
    for i in range(len(l)):
        l[i]="<"+tag+">"+l[i].strip()+"</"+tag+">\n"
    return l


@app.route('/taglist',methods=['POST','GET'])
# @login_required
def taglist():
    print request.method
    if request.method=='POST':

        rawtext=request.form['rawtext']
        tag=request.form['tag']
        formatted=addtagfx(rawtext, tag)
        app.logger.debug(formatted)
        resp = make_response(jsonify(success=True,title=request.form['rawtext']))
        return render_template('taglist.html', formatted=formatted)
    return render_template('taglist.html')



@app.route('/pills')
@login_required
def pills():
    
    return render_template('pills.html')

