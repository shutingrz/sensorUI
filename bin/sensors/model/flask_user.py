from sensors.model.ormutil import ORMUtil


class User(object):
    def __init__(self, user_hash):
        self.user_hash = user_hash

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_hash
