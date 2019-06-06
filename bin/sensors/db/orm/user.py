from sensors import db


class User(db.Model):

    __tablename__ = "user"
    username = db.Column(db.String(64), unique=True, nullable=False)
    user_hash = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(255))

    def __init__(self, username, user_hash, email):
        self.username = username
        self.user_hash = user_hash
        self.email = email


db.mapper(User, db.Table('user', db.metadata, autoload=True))
