
# flask-login 用クラス

class FlaskUser(object):
    def __init__(self, user_hash, username=None):
        self.user_hash = user_hash

        if username is not None:
            self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_hash

    def get_username(self):
        if self.username is None:
            return "名無し"
        else:
            return self.username
