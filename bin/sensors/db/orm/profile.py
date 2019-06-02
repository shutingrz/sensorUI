from sensors import db


class Profile(db.Model):

    __tablename__ = "profile"
    user_hash = db.Column(db.String(32), db.ForeignKey("user_hash.user_hash"))
    nickname = db.Column(db.String(16))

    userHash = db.relationship("UserHash")
    
    def __init__(self, user_hash, nickname):
        self.user_hash = user_hash
        self.nickname = nickname


db.mapper(Profile, db.Table('profile', db.metadata, autoload=True))
