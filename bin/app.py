#!/usr/bin/env python3

from flask import Flask, Blueprint
from cheers.controllers.cheers import cheers
from cheers.controllers.api import api as cheers_api
from cheers.util import Util

def create_app():

	app = Flask(__name__)
	try:
		app.config.from_pyfile('./cheers.conf')
	except FileNotFoundError as exc:
		app.logger.critical("'./cheers.conf' is not found.")
		raise FileNotFoundError(exc)

	try:
		dburl = app.config['DBURL']
		app.config['SQLALCHEMY_DATABASE_URI'] = dburl
		app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
	except KeyError as exc:
		app.logger.critical("DBURL is not set. please set dburl at cheers.conf!")
		raise KeyError(exc)
	
	app.config["SECRET_KEY"] = Util.generateRandomBytes(32)
	app.config['JSON_AS_ASCII'] = False
	app.config['WTF_CSRF_ENABLED'] = False

	Util.MaxUserIdLength = app.config["MAX_USERID_LENGTH"]
	Util.MaxUserPassLength = app.config["MAX_USERPASS_LENGTH"]
	Util.DefaultStockValue = app.config["DEFAULT_STOCK_VALUE"]
	Util.DebugMode = app.config["DEBUG_MODE"]
	Util.InfiniteMode = app.config["INFINITE_MODE"]

	app.register_blueprint(cheers)
	app.register_blueprint(cheers_api)

	return app

if __name__ == '__main__':
	app = create_app()
	app.run(debug=True, host=app.config['LISTEN'], port=app.config['PORT'])
