import os

##### Database Setup
#Dev
#SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI_DEV')


# if os.environ.get('SERVERTYPE')=='dev':
# 	# Use Dev database
# 	SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI_DEV')
# else:
# 	# Use Production database
# 	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Use production database (uncomment for override)
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
# DEBUG = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'my precious'
CSRF_ENABLED = True
WTF_CSRF_ENABLED = True

