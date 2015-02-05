import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
# DEBUG = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'my precious'
CSRF_ENABLED = True
WTF_CSRF_ENABLED = True

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

# Connect to the database
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
    },
}

# IMAGES_URL='/static/img/resized' #The url to mount Flask-Images to; defaults to '/imgsizer'.
# IMAGES_NAME= '/static/img'#The name of the registered endpoint used in url_for.
# IMAGES_PATH=['static/img'] #A list of paths to search for images (relative to app.root_path); e.g. ['static/uploads']
# IMAGES_CACHE='/tmp/flask-images' #Where to store resized images; defaults to '/tmp/flask-images'.
# IMAGES_MAX_AGE=3600# How long to tell the browser to cache missing results; defaults to 3600. Usually, we will set a max age of one year, and cache bust via the modification time of the source image.


# ### For Flask-Resize ###
# # Where your media resides
# RESIZE_ROOT = '/static/img/'

# # The URL where your media is served at. For the best performance you
# # should serve your media with a proper web server, under a subdomain
# # and with cookies turned off.
# RESIZE_URL = '/static/img/resized'