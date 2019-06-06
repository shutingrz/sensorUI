from sensors import db


class Authentication(db.Model):

    __tablename__ = "authentication"
    user_hash = db.Column(db.String(32), db.ForeignKey("user.user_hash"))
    encrypted_password = db.Column(db.String(64), nullable=False)
    hmac_key = db.Column(db.String(32), nullable=False)

    user = db.relationship("user")

    def __init__(self, user_hash, encrypted_password, hmac_key):
        self.user_hash = user_hash
        self.encrypted_password = encrypted_password
        self.hmac_key = hmac_key


db.mapper(Authentication, db.Table(
    'authentication', db.metadata, autoload=True))
