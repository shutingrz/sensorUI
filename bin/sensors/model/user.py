from flask import current_app
from sensors.util import Util
from sensors.model.flask_user import User as FlaskUser
from sensors.model.ormutil import ORMUtil
import sqlalchemy


class UserModel(object):

    def __init__(self):
        pass

    def user_isExist(self, user_id):
        db = ORMUtil.initDB()
        User = ORMUtil.getUserORM()

        if (db and User) is None:
            return None, 100

        try:
            user = db.session.query(User.user_id).filter(
                User.user_id == user_id).first()
        except Exception as exc:
            current_app.logger.critical(
                "user_isExist: Unknown error: %s" % exc)
            return None, 199

        if user is None:
            return False, 0
        else:
            return True, 0

    def user_register(self, user_id, password):
        db = ORMUtil.initDB()
        Authentication = ORMUtil.getAuthenticationORM()
        User = ORMUtil.getUserORM()

        if (db and Authentication and User) is None:
            return None, 100

        hmac_key = Util.generateRandomBytes(32)
        encrypted_password = Util.getEncryptedPassword(hmac_key, password)
        user_hash = Util.generateUserHash(user_id)

        try:
            db.session.add(Authentication(
                user_hash, encrypted_password, hmac_key))
            db.session.add(User(user_id, user_hash, email=None))
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as exc:
            current_app.logger.critical(
                "user_register: Integrity error: %s" % exc)
            return None, 110
        except Exception as exc:
            current_app.logger.critical(
                "user_register: Unknown error: %s" % exc)
            return None, 199

        return "ok", 0

    def user_delete(self, user_id):
        db = ORMUtil.initDB()
        Authentication = ORMUtil.getAuthenticationORM()
        User = ORMUtil.getUserORM()

        if (db and Authentication and User) is None:
            return None, 100

        try:
            user_hash = db.session.query(User.user_hash).filter(
                User.user_id == user_id).first().user_hash

            db.session.query(User).filter(User.user_hash == user_hash).delete()
            db.session.query(Authentication).filter(
                Authentication.user_hash == user_hash).delete()
            db.session.commit()
        except Exception as exc:
            current_app.logger.critical("user_delete: Unknown error: %s" % exc)
            return None, 199

        return "ok", 0

    def user_login(self, user_id, password):
        db = ORMUtil.initDB()
        Authentication = ORMUtil.getAuthenticationORM()
        User = ORMUtil.getUserORM()

        if (db and Authentication and User) is None:
            return None, 100

        try:
            user_hash = db.session.query(User.user_hash).filter(
                User.user_id == user_id).first().user_hash
            result = db.session.query(Authentication.hmac_key, Authentication.encrypted_password).filter(
                Authentication.user_hash == user_hash).first()
        except Exception as exc:
            current_app.logger.critical("user_login: Unknown error: %s" % exc)
            return None, 122

        if result is None:
            return None, 121

        hmac_key = result.hmac_key
        encrypted_password = Util.getEncryptedPassword(hmac_key, password)

        if result.encrypted_password == encrypted_password:
            try:
                return FlaskUser(user_hash), 0
            except Exception as exc:
                return None, 124
        else:
            return None, 123

    def user_list(self, page=None):
        db = ORMUtil.initDB()
        User = ORMUtil.getUserORM()

        if (db and User) is None:
            return None, 100

        try:
            result = db.session.query(User).all()
        except Exception as exc:
            current_app.logger.critical("user_list: Unknown error: %s" % exc)
            return None, 122

        users = []
        for user in result:
            user_dict = {"user_id": user.user_id}
            users.append(user_dict)

        return users, 0
