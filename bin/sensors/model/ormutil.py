import sqlalchemy
from sqlalchemy import asc, desc, or_
from flask import current_app
from sensors.util import Util

class ORMUtil(object):
	
	def __init__(self):
		pass

	@classmethod
	def initDB(self):
		try:
			from sensors import db
		except sqlalchemy.exc.OperationalError as exc:
			current_app.logger.critical("Database connection error: %s" % exc)
			return None
		except Exception as exc:
			current_app.logger.critical("Unknown OR/M error: %s" % exc)
			raise Exception(exc)

		return db

	@classmethod
	def getAuthenticationORM(self):
		try:
			from sensors.db.orm.authentication import Authentication
		except sqlalchemy.exc.NoSuchTableError as exc:
			current_app.logger.critical("authentication table is not exist.")
			return None
		except Exception as exc:
			current_app.logger.critical("Unknown OR/M error: %s" % exc)
			raise Exception(exc)

		return Authentication

	@classmethod
	def getUserORM(self):
		try:
			from sensors.db.orm.user import User
		except sqlalchemy.exc.NoSuchTableError as exc:
			current_app.logger.critical("user table is not exist.")
			return None
		except Exception as exc:
			current_app.logger.critical("Unknown OR/M error: %s" % exc)
			raise Exception(exc)

		return User

	@classmethod
	def getProfileORM(self):
		try:
			from sensors.db.orm.profile import Profile
		except sqlalchemy.exc.NoSuchTableError as exc:
			current_app.logger.critical("profile table is not exist.")
			return None
		except Exception as exc:
			current_app.logger.critical("Unknown OR/M error: %s" % exc)
			raise Exception(exc)

		return Profile

	@classmethod
	def getUserHashORM(self):
		try:
			from sensors.db.orm.user_hash import UserHash
		except sqlalchemy.exc.NoSuchTableError as exc:
			current_app.logger.critical("user_hashtable is not exist.")
			return None
		except Exception as exc:
			current_app.logger.critical("Unknown OR/M error: %s" % exc)
			raise Exception(exc)

		return UserHash
