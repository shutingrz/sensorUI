from sensors import db


class Profile(db.Model):
    def __init__(self, user_id, nickname):
        self.user_id = user_id
        self.nickname = nickname


db.mapper(Profile, db.Table('profile', db.metadata, autoload=True))
