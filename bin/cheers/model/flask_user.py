from cheers.model.ormutil import ORMUtil

class User(object):
	def __init__(self, user_id):
		self.user_id = user_id
		self.__set_profile(user_id)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.user_id

	def __set_profile(self, user_id):
		db = ORMUtil.initDB()
		Profile = ORMUtil.getProfileORM()

		if (db and Profile) is None:
			return user_id

		try:
			result = db.session.query(Profile).filter(Profile.user_id == user_id).first()
		except Exception as exc:
			self.nickname = user_id
			self.department = "現在参照できません"

		if result.nickname is None:
			self.nickname = user_id
		else:
			self.nickname = result.nickname

		if result.department is None:
			self.department = "所属未設定"
		else:
			self.department = result.department

