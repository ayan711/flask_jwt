from flask import Flask ,jsonify
from . import models
from src.models import db
import os
from .utils.http_status_code import *

from src.auth import auth
from src.books import books

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY='004f2af45d3a4e161a7dd2d17fdae47f',
            SQLALCHEMY_DATABASE_URI='sqlite:///../bookstore.db',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY='004f2af45d3a4e161a7dd2d17fdae47f',


            SWAGGER={
                'title': "Bookmarks API",
                'uiversion': 3
            }
        )
        
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    
    @app.route('/')
    def hello():
        return jsonify({"message":"Hello World!"}),HTTP_200_OK
    
    app.register_blueprint(auth)
    app.register_blueprint(books)

    return app