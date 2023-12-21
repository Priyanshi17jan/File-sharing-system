# app/__init__.py
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_pyfile('config.py')
mongo = PyMongo(app)
jwt = JWTManager(app)

from app.ops_routes import ops_bp
from app.client_routes import client_bp

app.register_blueprint(ops_bp, url_prefix='/ops')
app.register_blueprint(client_bp, url_prefix='/client')
