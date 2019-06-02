from flask import current_app
from cheers.model.ormutil import ORMUtil

class AccountModel(object):
	
	def __init__(self):
		pass

	def account_status(self, user_id):
		db = ORMUtil.initDB()
		User = ORMUtil.getUserORM()

		if (db and User) is None:
			return None, 100

		try:
			result = db.session.query(User.gift, User.stock).filter(User.user_id == user_id).first()
		except Exception as exc:
			return None, 122

		if result is None:
			return None, 121
			
		msg = {"receive Like": result.gift, "stock Like": result.stock}

		return msg, 0

	def account_save_profile(self, user_id, nickname=None, email=None, department=None, introduction=None):
		db = ORMUtil.initDB()
		Profile = ORMUtil.getProfileORM()

		if (db and Profile) is None:
			return None, 100

		#プロフィール取得
		try:
			result = db.session.query(Profile).filter(Profile.user_id == user_id).first()
		except Exception as exc:
			return None, 141

		if result is None:
			return None, 145

		#変更しない値は現在の値を使う(=>変更なし)
		if nickname is None:
			nickname = result.nickname
		if email is None:
			email = result.email
		if department is None:
			department = result.department
		if introduction is None:
			introduction = result.introduction

		#コミット
		try:
			db.session.query(Profile).filter(Profile.user_id == user_id).update({'nickname': nickname, 'email': email, 'department': department, 'introduction': introduction})
			db.session.commit()
		except Exception as exc:
			return None, 143

		return "ok", 0
			
