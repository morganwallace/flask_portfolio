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
from easy_thumbnails import get_thumbnailer
thumb_url = get_thumbnailer(profile.photo)['avatar'].url