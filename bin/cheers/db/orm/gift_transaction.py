from cheers import db

class GiftTransaction(db.Model):
	def __init__(self, sender, receiver, value, message, is_anonymous, created_at):
			self.sender = sender
			self.receiver = receiver
			self.value = value
			self.message = message
			self.is_anonymous = is_anonymous
			self.created_at = created_at

db.mapper(GiftTransaction, db.Table('gift_transaction', db.metadata, autoload=True))
