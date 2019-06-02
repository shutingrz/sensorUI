import sqlalchemy
from sqlalchemy import asc, desc, or_
from flask import current_app
from cheers.util import Util

class ORMUtil(object):
	
	def __init__(self):
		pass

	@classmethod
	def initDB(self):
		try:
			from cheers import db
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
			from cheers.db.orm.authentication import Authentication
		except sqlalchemy.exc.NoSuchTableError as exc:
			current_app.logger.critical("table is not exist.")
			return None
		except Exception as exc:
			current_app.logger.critical("Unknown OR/M error: %s" % exc)
			raise Exception(exc)

		return Authentication

	@classmethod
	def getUserORM(self):
		try:
			from cheers.db.orm.user import User
		except sqlalchemy.exc.NoSuchTableError as exc:
			current_app.logger.critical("table is not exist.")
			return None
		except Exception as exc:
			current_app.logger.critical("Unknown OR/M error: %s" % exc)
			raise Exception(exc)

		return User

	@classmethod
	def getProfileORM(self):
		try:
			from cheers.db.orm.profile import Profile
		except sqlalchemy.exc.NoSuchTableError as exc:
			current_app.logger.critical("table is not exist.")
			return None
		except Exception as exc:
			current_app.logger.critical("Unknown OR/M error: %s" % exc)
			raise Exception(exc)

		return Profile

	@classmethod
	def getUserHashORM(self):
		try:
			from cheers.db.orm.user_hash import UserHash
		except sqlalchemy.exc.NoSuchTableError as exc:
			current_app.logger.critical("table is not exist.")
			return None
		except Exception as exc:
			current_app.logger.critical("Unknown OR/M error: %s" % exc)
			raise Exception(exc)

		return UserHash

	@classmethod
	def getGiftTransactionORM(self):
		try:
			from cheers.db.orm.gift_transaction import GiftTransaction
		except sqlalchemy.exc.NoSuchTableError as exc:
			current_app.logger.critical("table is not exist.")
			return None
		except Exception as exc:
			current_app.logger.critical("Unknown OR/M error: %s" % exc)
			raise Exception(exc)

		return GiftTransaction
