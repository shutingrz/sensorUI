from cheers import db

class UserHash(db.Model):
	def __init__(self, user_id, user_hash):
			self.user_id = user_id
			self.user_hash = user_hash

db.mapper(UserHash, db.Table('user_hash', db.metadata, autoload=True))
