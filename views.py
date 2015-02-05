from flask import session, request, make_response, jsonify, flash, url_for, redirect,g,render_template,Flask, abort ,g
from flask.ext.sqlalchemy import SQLAlchemy

import os,time
from datetime import date
#### views (Home, Project pages, etc)
##############
from app import app
from manage import db, Project, User

from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from flask.ext.openid import OpenID
oid = OpenID(app, os.path.join('tmp'))




from forms import LoginForm

# index view function suppressed for brevity

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
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
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))


######  Miguel Grinberg's login 

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for OpenID="%s", remember_me=%s' %
#               (form.openid.data, str(form.remember_me.data)))
#         return redirect('/index')
#     return render_template('login.html', 
#                            title='Sign In',
#                            form=form,
#                            providers=app.config['OPENID_PROVIDERS'])


@app.route('/')
def home():
    projects=db.session.query(Project.title,Project.body,Project.projectType,Project.tags,Project.externalLink,Project.imagesLinks,Project.snippet,Project.date).all()
    # all_users = User.query.all()
    projectsList=[]

    for proj in projects:

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
def admin():
    return render_template('admin.html')

@app.route('/project/<title>')
def project(title):
    title=title.replace("-"," ")
    myproject=db.session.query(Project.title,Project.body,Project.projectType,Project.tags,Project.externalLink,Project.imagesLinks,Project.date,Project.cover_photo,Project.codeLink).filter(Project.title==title.lower()).first()
    app.logger.debug(myproject)
    app.logger.debug(title)
    title=str(myproject[0]).title()
    app.logger.debug(myproject[5].split(","))
    if myproject[7]!=None:
        coverphoto= myproject[7].split(",")
    else:
        coverphoto=None

    print myproject[8]
    return render_template('project.html',
        title=title, 
        body=myproject[1],
        projectType=myproject[2],
        tags=myproject[3].split(","),
        externalLink=myproject[4],
        imagesLinks=myproject[5].split(","),
        pageTitle=title+" - Morgan Wallace",
        date=date.fromtimestamp(myproject[6]*24*3600).strftime("%b %d, %Y"),
        coverphoto=coverphoto,
        codelink=myproject[8]
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
            'imagesLinks':url_for('static',filename='img/'+proj[5].split(",")[0]), #only take first photo
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
