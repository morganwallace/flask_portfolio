from flask import session, request, make_response, jsonify, flash, url_for, redirect,g,render_template,Flask
from flask.ext.sqlalchemy import SQLAlchemy

import os



app = Flask(__name__)

# Loads configuration from `config.py`
app.config.from_object('config')

# see http://flask.pocoo.org/docs/0.10/errorhandling/#when-in-doubt-run-manually
if os.environ.get('SERVERTYPE')=='dev':
	app.debug = True

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')

from views import *

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    #to run a debug mode only when developing locally run this in terminal:
    # $ export SERVERTYPE="dev"

    app.run(host='0.0.0.0', port=port)
