import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'my precious'
CSRF_ENABLED = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = "postgres://ayzcctpvbmwajn:z1bTq5u6fbqWmGFHR0UrOpN_zW@ec2-54-197-249-167.compute-1.amazonaws.com:5432/d25indqqmd1654"