from flask import session, request, make_response, jsonify, flash, url_for, redirect,g,render_template,Flask
from flask.ext.sqlalchemy import SQLAlchemy

import os,time
from datetime import date

from config import basedir


app = Flask(__name__)

# Loads configuration from `config.py`
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')

from views import *

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    #to run a debug mode only when developing locally run this in terminal:
    # $ export SERVERTYPE="dev"

    if os.environ.get('SERVERTYPE')=='dev':
        app.debug = True


    app.run(host='0.0.0.0', port=port)
