from flask import current_app
import sqlalchemy
from app import db
from app.util import Util, ResultCode
from app.model.flask_user import FlaskUser
from app.db.orm import Authentication, User



class UserModel(object):

    def __init__(self):
        pass

    def user_isExist(self, username):

        try:
            user = db.session.query(User.username).filter(
                User.username == username).first()        
        except Exception as exc:
            current_app.logger.critical(
                "user_isExist: Unknown error: %s" % exc)
            return None, ResultCode.DBError

        if user is None:
            return False, ResultCode.Success
        else:   
            return True, ResultCode.Success


    def user_register(self, username, password):

        hmac_key = Util.generateRandomBytes(32)
        encrypted_password = Util.getEncryptedPassword(hmac_key, password)
        user_hash = Util.generateUserHash(username)

        try:
            db.session.add(User(username, user_hash, email=None))
            db.session.add(Authentication(
                user_hash, encrypted_password, hmac_key))    
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as exc:
            current_app.logger.critical(
                "user_register: Integrity error: %s" % exc)
            return None, ResultCode.FormatError
        except Exception as exc:
            current_app.logger.critical(
                "user_register: Unknown error: %s" % exc)
            return None, ResultCode.DBError

        return "ok", ResultCode.Success

    def user_delete(self, username):

        try:
            user_hash = db.session.query(User.user_hash).filter(
                User.username == username).first().user_hash

            db.session.query(User).filter(User.user_hash == user_hash).delete()
            db.session.query(Authentication).filter(
                Authentication.user_hash == user_hash).delete()
            db.session.commit()
        except Exception as exc:
            current_app.logger.critical("user_delete: Unknown error: %s" % exc)
            return None, ResultCode.DBError

        return "ok", ResultCode.Success

    def user_login(self, username, password):
        try:
            user_result = db.session.query(User).filter(
                User.username == username).first()

            if not user_result:
                return None, ResultCode.ValueError

            user_hash = user_result.user_hash

            result = db.session.query(Authentication.hmac_key, Authentication.encrypted_password).filter(
                Authentication.user_hash == user_hash).first()

        except Exception as exc:
            current_app.logger.critical("user_login: Unknown error: %s" % exc)
            return None, ResultCode.DBError

        if result is None:
            return None, ResultCode.ValueError

        hmac_key = result.hmac_key
        encrypted_password = Util.getEncryptedPassword(hmac_key, password)

        if result.encrypted_password == encrypted_password:
            return FlaskUser(user_hash, username), ResultCode.Success
        else:
            return None, ResultCode.ValueError

    def getUsername(self, user_hash):

        try:
            username = db.session.query(User.username).filter(
                User.user_hash == user_hash).first().username
        except Exception as exc:
            current_app.logger.critical("getUsername: Unknown error: %s" % exc)
            return None

        return username

    def user_list(self, page=None):

        try:
            result = db.session.query(User).all()
        except Exception as exc:
            current_app.logger.critical("user_list: Unknown error: %s" % exc)
            return None, ResultCode.DBError

        users = []
        for user in result:
            user_dict = {"username": user.username}
            users.append(user_dict)

        return users, ResultCode.Success
