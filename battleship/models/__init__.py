from os import path

from flask_sqlalchemy import SQLAlchemy

from battleship import api

from boltfile import PROJECT_ROOT


api.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(PROJECT_ROOT, 'data.db')
api.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
api.app.config['SQLALCHEMY_RECORD_QUERIES'] = True

db = SQLAlchemy()
