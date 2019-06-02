from cheers import db

class User(db.Model):
	def __init__(self, user_id, email, gift, stock):
			self.user_id = user_id
			self.email = email
			self.gift = gift
			self.stock = stock

db.mapper(User, db.Table('user', db.metadata, autoload=True))
