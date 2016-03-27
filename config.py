import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
syncer_admin_key = ''
app_logfile = os.path.join(basedir, 'debug.html')
