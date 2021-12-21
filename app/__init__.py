from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from api import main

db = SQLAlchemy()
class Photos(db.Model):
    id = db.Column(db.String(21), primary_key=True)
    prediction = db.Column(db.Integer, nullable=True)
    data = db.Column(db.PickleType, nullable=True)
    date = db.Column(db.DateTime, nullable=False)

def create_app():
    flaskapp = Flask(__name__)
    flaskapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photos.db'
    flaskapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(flaskapp)
    with flaskapp.app_context():
        db.create_all()
    from .apie import endpoints
    flaskapp.register_blueprint(endpoints)
    return flaskapp