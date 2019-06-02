from sensors import db


class User(db.Model):

	__tablename__ = "user"
	user_id = db.Column(db.String(64), unique=True, nullable=False)
	email = db.Column(db.String(255))
	
	def __init__(self, user_id, email):
		self.user_id = user_id
		self.email = email


db.mapper(User, db.Table('user', db.metadata, autoload=True))
