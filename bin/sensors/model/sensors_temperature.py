import sqlalchemy
from sqlalchemy import or_
from flask import current_app
from sensors.util import Util
from sensors.model.ormutil import ORMUtil


class SensorTemperatureModel(object):

    def __init__(self):
        pass

    def view(self, user_hash, device_id):
        msg = {"data": "unimplemented function"}
        return msg, 0

    def record(api_key, time, value):
        msg = {"data": "unimplemented function"}
        return msg, 0
