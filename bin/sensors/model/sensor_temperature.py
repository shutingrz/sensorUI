import sqlalchemy
from sqlalchemy import or_, desc
from flask import current_app
from sensors.util import Util
from sensors.model.ormutil import ORMUtil


class SensorTemperatureModel(object):

    def __init__(self):
        pass

    def view(self, user_hash, device_id):
        db = ORMUtil.initDB()
        Temperature = ORMUtil.getSensorTemperatureORM()
        Device = ORMUtil.getDeviceORM()

        if (db and Temperature and Device) is None:
            return None, 100
        
        try:
            devicelist = db.session.query(Device.device_id)\
                                .filter(Device.user_hash == user_hash)\
                                .filter(Device.device_id == device_id)\
                                .all()

            if not devicelist :
                msg = "this device is not yours"
                return msg, 110

            result = db.session.query(Temperature)\
                                .filter(Temperature.device_id == device_id)\
                                .order_by(desc(Temperature.time))\
                                .limit(10)\
                                .all()
                                
        except Exception as exc:
            current_app.logger.critical("Unknown error: %s" % exc)
        
        records = []
        for record in result:
            record_dict = {"time": record.time, "value": record.temperature}
            records.append(record_dict)


        return records, 0

    def record(api_key, time, value):
        msg = {"data": "unimplemented function"}
        return msg, 0
