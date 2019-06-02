from sensors import db

class UserHash(db.Model):

	__tablename__ = "user_hash"
	user_id = db.Column(db.String(64), db.ForeignKey("user.user_id"))
	user_hash = db.Column(db.String(32))

	user = db.relationship("user")

	def __init__(self, user_id, user_hash):
			self.user_id = user_id
			self.user_hash = user_hash

db.mapper(UserHash, db.Table('user_hash', db.metadata, autoload=True))
