from sensors import db

class Authentication(db.Model):

	__tablename__ = "authentication"
	user_id = db.Column(db.String(64), db.ForeignKey("user.user_id"))
	encrypted_password = db.Column(db.String(64), nullable=False)
	hmac_key = db.Column(db.String(32), nullable=False)

	user = db.relationship("user")

	def __init__(self, user_id, encrypted_password, hmac_key):
			self.user_id = user_id
			self.encrypted_password = encrypted_password
			self.hmac_key = hmac_key

db.mapper(Authentication, db.Table('authentication', db.metadata, autoload=True))
