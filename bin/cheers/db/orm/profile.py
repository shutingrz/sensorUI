from cheers import db

class Profile(db.Model):
	def __init__(self, user_id, nickname, icon_path, email, department, introduction):
			self.user_id = user_id
			self.nickname = nickname
			self.icon_path = icon_path
			self.email = email
			self.department = department
			self.introduction = introduction

db.mapper(Profile, db.Table('profile', db.metadata, autoload=True))
