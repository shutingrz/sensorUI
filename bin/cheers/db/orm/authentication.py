from cheers import db

class Authentication(db.Model):
	def __init__(self, user_id, encrypted_password, hmac_key):
			self.user_id = user_id
			self.encrypted_password = encrypted_password
			self.hmac_key = hmac_key

db.mapper(Authentication, db.Table('authentication', db.metadata, autoload=True))
