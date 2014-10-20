from flask import Flask
from flask import render_template
from flask import session, request, make_response, jsonify, flash, url_for, redirect,g
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
from flask.ext.login import login_user, LoginManager, logout_user, current_user, login_required
from flask.ext.openid import OpenID
import os

app = Flask(__name__)


# Loads configuration from `config.py`
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ayzcctpvbmwajn:z1bTq5u6fbqWmGFHR0UrOpN_zW@ec2-54-197-249-167.compute-1.amazonaws.com:5432/d25indqqmd1654"

####### Database classes/schema
from manage import db, User, Project

basedir = os.getcwd()
login_manager = LoginManager()
login_manager.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         # login and validate the user...
#         login_user(user)
#         flash("Logged in successfully.")
#         return redirect(request.args.get("next") or url_for("index"))
#     return render_template("login.html", form=form)


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' in request.cookies:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('signup'))
    return wrap


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(home)



@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])


########  Routing

@app.route('/')
def home():
    projects=db.session.query(Project.title, Project.body,Project.projectType,Project.tags).all()
    # all_users = User.query.all()
    app.logger.debug(projects)
    # user_id = request.cookies.get('user_id')
    # flash('Your user id is: '+user_id)
    return render_template('index.html')

## add admin.html soon
# @app.route('/admin')
# def admin():
#     return render_template('admin.html')

@app.route('/add')
@login_required
def add():
    # all_users = User.query.all()
    # app.logger.debug( all_users)
    # user_id = request.cookies.get('user_id')
    # flash('Your user id is: '+user_id)
    return render_template('add.html')


@app.route('/adduser' , methods=['POST'])
def add_user():
    user_info=request.form
    app.logger.debug(user_info)
    user = User(firstname=user_info['firstname'],
        lastname=user_info['lastname'],
        email=user_info['email'],
        username=user_info['username'],
        password=password)
    
    #query database for unique email
    test = User.query.filter_by(email=user_info['email']).first()
    app.logger.debug(test)
    if test is None:
        #add record for new user
        app.logger.debug('new user')
        db.session.add(user)
        db.session.commit()
        resp = make_response(jsonify(success=True))

        #eventually make the cookie a token
        resp.set_cookie({'user_id': user.id,'username':user_info['username'],'fname':user_info['firstname']})
    else: 
        app.logger.debug('existing user')
        resp = make_response(jsonify(success=False,existing_email=user_info['email']))
    return resp
    #if user is new add it

@app.route('/signin' , methods=['POST'])
def signin():
    test=User.query.filter_by(username=request.form['username'])
    if test is not None:
        resp = make_response(jsonify(success=True))
        resp.set_cookie('user_id', user.id)
    else: 
        app.logger.debug('no username')
        resp = make_response(jsonify(success=False))
    return resp


@app.route('/addproject' , methods=['POST'])
def add_project():
    app.logger.debug("/addproject in app.py:\n"+str(request.form))
    user_id = request.cookies.get('user_id')
    # app.logger.debug(user_id)
    #args to init a project: title, body,user_id,project_type,tags
    #add to database
    project= Project(
        title=request.form['title'],
        body=request.form['body'],
        user_id=user_id,
        projectType=request.form['projectType'],
        tags=request.form['tags'],
        externalLink=request.form['externalLink'],
        imagesLink=request.form['imagesLink']
        )
    db.session.add(project)
    db.session.commit()
    app.logger.debug("Successfully project added to database")
    resp = make_response(jsonify(success=True,title=request.form['title']))
    return resp



@app.route('/project/<title>')
def project(title):
    myproject=db.session.query(Project.title,Project.body,Project.projectType,Project.tags,Project.externalLink,Project.imagesLink).filter(Project.title==title).first()
    # app.logger.debug('opening /project/'+title+'\n'+project.all())
    return render_template('project.html',
        title=myproject[0], 
        body=myproject[1],
        projectType=myproject[2],
        tags=myproject[3],
        externalLink=myproject[4],
        imagesLink=myproject[5])   



@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404




if __name__ == '__main__':
    app.run(debug=True)

