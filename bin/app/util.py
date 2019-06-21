import hmac
import hashlib
import string
import secrets
from enum import Enum, IntEnum, auto

class ResultCode(IntEnum):
    Success = 0
    DBError = auto()
    FormatError = auto()
    ValueError = auto()
    GenericError = auto()


class Util():

    class NotificationType():
        Primary = "primary"
        Success = "success"
        Warning = "warning"
        Danger = "Danger"


    class SensorType():
        Temperature = 1

    MaxUsernameLength = 64
    MaxUserPassLength = 64
    DebugMode = True

    @classmethod
    def generateNotificationMessage(self, status, message):
        return {"status": status, "message": message, "pos": 'top-center'}
        

    @classmethod
    def generateRandomBytes(self, length, seq=string.digits + string.ascii_lowercase):
        rand_str = ''.join(secrets.choice(
            string.ascii_letters + string.digits) for i in range(length))
        rand_bytes = rand_str.encode('ascii')
        return rand_bytes

    @classmethod
    def generateRandomString(self, length, seq=string.digits + string.ascii_lowercase):
        rand_str = ''.join(secrets.choice(
            string.ascii_letters + string.digits) for i in range(length))
        return rand_str

    @classmethod
    def getEncryptedPassword(self, key, password):
        password_bytes = password.encode('utf-8')
        return hmac.new(key, password_bytes, hashlib.sha256).hexdigest()

    @classmethod
    def generateUserHash(self, username):
        key = self.generateRandomBytes(32)
        username_bytes = username.encode('utf-8')
        userHash = hmac.new(key, username_bytes, hashlib.md5).hexdigest()
        return userHash

