# Flask-Based Portfolio

This is a Python web app for showcasing your projects.
##Underlying technology

#### Backend
* Flask
* Heroku
* Postgres

#### Frontend
* Bootsrap 3.0
* Jinja2 (templating)
* jQuery




##Installation
####Step 1 - clone from github
Use the following unix commands to install:
*If you don't have **virualenv** installed, use this command to install it before continuing.

	$ git clone git@github.com:morganwallace/flask_portfolio.git && cd flask-portfolio

Now that you have it downloaded, create a vitual environment to isolate the Python libraries for this project (you'll do this each time)

	$ virtualenv venv
	$ source venv/bin/activate 
	$ pip install -r requirements.txt

####Step 2 - setup heroku
Install the [Heroku toolbelt](https://toolbelt.heroku.com/) if you haven't already. 

Log in if you haven't already

	$ heroku login
	
After loging in, create a heroku app:

	$ heroku create


####Step 3 - setup database
Add a PostgreSQL database from Heroku. More info here <https://addons.heroku.com/heroku-postgresql>

	$ heroku addons:add heroku-postgresql
	
Take that postgres URI and set it as an environment variable (don't share it unless you want to share your whole database):

	$ echo $SHELL 
If you're running bash:

	$ nano ~/.bashrc
	
or if you're running Zsh:

	$ nano ~/.zshrc
	
In either case put these 2 environment variables in the rc file of whichever shell you use like so:

	export DB_URI="postgres://..."
	export SERVERTYPE='dev'

*The second line ensures that you are in debug mode only when developing locally, not once you deploy*

Next, add the database URI to heroku too:

	$ heroku config:set DB_URI=postgres://...

This app uses SQL Alchemy to make database interactions easier. It also uses [Flask-Migrate](http://blog.miguelgrinberg.com/post/flask-migrate-alembic-database-migration-wrapper-for-flask), an extension that makes it easier to update the database models (schema). We must initialize the migrations:

	$ python manage.py db init

Now we can syncronize our models with our database by running these 2 commands:

	$ $ python manage.py db migrate
	$ $ python manage.py db upgrade
	
- I simplified this by making the `update_database.command` file, which does the same as the above 2 commands but can be run by clicking on it or from the command line.
- **Important**: You should run `update_database.command` everytime you change your database models in order to change the heroku postgres database.


####Step 5 - add, commit, and push (deploy) to heroku

Lastly, use git to add, commit, and push to heroku

	$ git add .
	$ git commit -m "first commit"
	$ git push heroku master

**Done!!!** 

*whenever you want to push new changes, follow step 5 (for changes to the database, run the `updated_database.command`)*

-----

## Run local server for development
1. ``$ source venv/bin/activate``
2. ``$ python app.py``
3. preview at http://localhost:5000/


---

##### Installed Packages (requirements.txt)
Flask==0.9
Flask-KVSession==0.6.1
Flask-Login==0.2.11
Flask-Mail==0.9.0
Flask-Migrate==1.2.0
Flask-OpenID==1.2.1
Flask-SQLAlchemy==1.0
Flask-Script==2.0.5
Flask-WTF==0.9.5
Jinja2==2.6
Mako==1.0.0
MarkupSafe==0.23
SQLAlchemy==0.7.8
WTForms==1.0.5
Werkzeug==0.8.3
alembic==0.6.5
blinker==1.3
itsdangerous==0.24
psycopg2==2.4.5
python-openid==2.2.5
pytz==2014.4
simplekv==0.9.2
six==1.7.3
virtualenv==1.11.6
wsgiref==0.1.2
