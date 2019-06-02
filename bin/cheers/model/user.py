from flask import current_app
from cheers.util import Util
from cheers.model.flask_user import User as FlaskUser
from cheers.model.ormutil import ORMUtil

class UserModel(object):
	
	def __init__(self):
		pass

	def user_isExist(self, user_id):
		db = ORMUtil.initDB()
		User = ORMUtil.getUserORM()

		if (db and User) is None:
			return None, 100

		try:
			user = db.session.query(User.user_id).filter(User.user_id == user_id).first()
		except Exception as exc:
			current_app.logger.critical("user_isExist: Unknown error: %s" % exc)
			return None, 199
			
		if user is None:
			return False, 0
		else:
			return True, 0

	def user_register(self, user_id, password):
		db = ORMUtil.initDB()
		Authentication = ORMUtil.getAuthenticationORM()
		User = ORMUtil.getUserORM()
		UserHash = ORMUtil.getUserHashORM()
		Profile = ORMUtil.getProfileORM()

		if (db and Authentication and User and UserHash and Profile) is None:
			return None, 100

		hmac_key = Util.generateRandomBytes(32)
		encrypted_password = Util.getEncryptedPassword(hmac_key, password)
		user_hash = Util.generateUserHash(user_id)

		try:
			db.session.add(Authentication(user_id, encrypted_password, hmac_key))
			db.session.add(User(user_id, email=None, gift=0, stock=Util.DefaultStockValue))
			db.session.add(UserHash(user_id, user_hash))
			db.session.add(Profile(user_id, nickname=None, icon_path=None, email=None, department=None, introduction=None))
			db.session.commit()
		except sqlalchemy.exc.IntegrityError as exc:
			current_app.logger.critical("user_register: Integrity error: %s" % exc)
			return None, 110
		except Exception as exc:
			current_app.logger.critical("user_register: Unknown error: %s" % exc)
			return None, 199

		return "ok", 0
		
	def user_delete(self, user_id):
		db = ORMUtil.initDB()
		Authentication = ORMUtil.getAuthenticationORM()
		User = ORMUtil.getUserORM()
		UserHash = ORMUtil.getUserHashORM()
		Profile = ORMUtil.getProfileORM()

		if (db and Authentication and User and Profile) is None:
			return None, 100

		try:
			db.session.query(Profile).filter(Profile.user_id == user_id).delete()
			db.session.query(User).filter(User.user_id == user_id).delete()
			db.session.query(UserHash).filter(UserHash.user_id == user_id).delete()
			db.session.query(Authentication).filter(Authentication.user_id == user_id).delete()
			db.session.commit()
		except Exception as exc:
			current_app.logger.critical("user_delete: Unknown error: %s" % exc)
			return None, 199
		
		return "ok", 0

	def user_login(self, user_id, password):
		db = ORMUtil.initDB()
		Authentication = ORMUtil.getAuthenticationORM()
		Profile = ORMUtil.getProfileORM()

		if (db and Authentication and Profile) is None:
			return None, 100

		try:
			result = db.session.query(Authentication.hmac_key, Authentication.encrypted_password).filter(Authentication.user_id == user_id).first()
		except Exception as exc:
			return None, 122

		if result is None:
			return None, 121

		hmac_key = result.hmac_key.encode('ascii')
		encrypted_password = Util.getEncryptedPassword(hmac_key, password)

		if result.encrypted_password == encrypted_password:
			try:
				result = db.session.query(Profile.nickname).filter(Profile.user_id == user_id).first()
				if result.nickname is None:
					return FlaskUser(user_id), 0
				else:
					return FlaskUser(user_id), 0
			except Exception as exc:
				return None, 124
		else:
			return None, 123

	def user_list(self, page=None):
		db = ORMUtil.initDB()
		Profile = ORMUtil.getProfileORM()

		if (db and Profile) is None:
			return None, 100

		try:
			result = db.session.query(Profile).all()
		except Exception as exc:
			return None, 122

		users = []
		for user in result:
			user_dict = {"user_id": user.user_id, "nickname": user.nickname, "icon_path": user.icon_path, "department": user.department, "introduction": user.introduction}
			users.append(user_dict)

		return users, 0


	def user_profile(self, user_id):
		db = ORMUtil.initDB()
		Profile = ORMUtil.getProfileORM()

		if (db and Profile) is None:
			return None, 100

		try:
			result = db.session.query(Profile).filter(Profile.user_id == user_id).first()
		except Exception as exc:
			return None, 141

		if result is None:
			return None, 142

		msg = {"user_id": result.user_id, "nickname": result.nickname, "icon_path": result.icon_path, "email": result.email, "department": result.department, "introduction": result.introduction}
		
		return msg, 0
		
