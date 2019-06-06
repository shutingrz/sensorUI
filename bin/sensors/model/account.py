from flask import current_app
from sensors.model.ormutil import ORMUtil


class AccountModel(object):

    def __init__(self):
        pass

    def account_status(self, user_hash):
        db = ORMUtil.initDB()
        User = ORMUtil.getUserORM()

        if (db and User) is None:
            return None, 100

        msg = {"data": "removed function"}

        return msg, 0
