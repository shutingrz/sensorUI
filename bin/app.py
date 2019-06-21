#!/usr/bin/env python3

from flask import Flask, Blueprint
from sensors.controllers.api import api
from sensors.controllers.webui import webui
from sensors.util import Util
from flask_wtf.csrf import CSRFProtect
from sensors.db import init_db
from sensors import db
from flask_sqlalchemy import SQLAlchemy

def create_app(DBURL=None):

    app = Flask(__name__)

    csrf = CSRFProtect(app)
    csrf.init_app(app)

    try:
        app.config.from_pyfile('./sensors.conf')
    except FileNotFoundError as exc:
        app.logger.critical("'./sensors.conf' is not found.")
        raise FileNotFoundError(exc)

    try:
        if DBURL is not None:
            dburl = DBURL
        else:
            dburl = app.config['DBURL']

        app.config['SQLALCHEMY_DATABASE_URI'] = dburl
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    except KeyError as exc:
        app.logger.critical(
            "DBURL is not set. please set dburl at sensors.conf!")
        raise KeyError(exc)

    app.config["SECRET_KEY"] = Util.generateRandomBytes(32)
    app.config['JSON_AS_ASCII'] = False

    Util.MaxUsernameLength = app.config["MAX_USERID_LENGTH"]
    Util.MaxUserPassLength = app.config["MAX_USERPASS_LENGTH"]
    Util.DebugMode = app.config["DEBUG_MODE"]

    app.register_blueprint(api)
    app.register_blueprint(webui)

    return app


app = create_app()
init_db(app)

# Migrate対応だが一旦 db.create_all() をする運用とする
with app.app_context():
	db.create_all()


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG_MODE"], 
            host=app.config['LISTEN'], 
            port=app.config['PORT']
        )
