import sqlalchemy
from sqlalchemy import or_, desc
from flask import current_app
from sensors.util import Util
from datetime import datetime, timedelta

from sensors import db
from sensors.db.orm.device import Device
from sensors.db.orm.sensor_temperature import SensorTemperature

class SensorTemperatureModel(object):

    def __init__(self):
        pass

    def view(self, user_hash, device_id, startTime=0, endTime=int(datetime.now().timestamp())):

        try:
            device_result = db.session.query(Device.device_id)\
                .filter(Device.user_hash == user_hash)\
                .filter(Device.device_id == device_id)\
                .first()

            if not device_result:
                msg = "this device is not yours"
                return msg, 110

            result = db.session.query(SensorTemperature)\
                .filter(SensorTemperature.device_id == device_id)\
                .filter(SensorTemperature.time > startTime)\
                .filter(SensorTemperature.time < endTime)\
                .order_by(desc(SensorTemperature.time))\
                .limit(100)\
                .all()

        except Exception as exc:
            current_app.logger.critical("Unknown error: %s" % exc)

        records = []
        for record in result:
            record_dict = {"time": record.time, "value": record.temperature}
            records.append(record_dict)

        return records, 0

    def getDataOfLastTenMinutes(self, user_hash, device_id):
        now = datetime.now()
        minusTenMinutes = now - timedelta(minutes=10)

        startTime = int(minusTenMinutes.timestamp())
        endTime = int(now.timestamp())
        
        record, code = self.view(user_hash, device_id, startTime=startTime, endTime=endTime)    

        return record, code


    def record(self, api_key, time, value):

        try:
            device_result = db.session.query(Device)\
                .filter(Device.api_key == api_key)\
                .first()

            if not device_result:
                msg = "device data is not found"
                return msg, 110

            device_id = device_result.device_id

            db.session.add(SensorTemperature(
                device_id=device_id,
                time=time,
                temperature=value
            ))

            db.session.commit()

        except Exception as exc:
            current_app.logger.critical("Unknown error: %s" % exc)
            return None, 199

        msg = "ok"
        return msg, 0


    def deleteAll(self, user_hash, device_id):

        try:
            #デバイス登録情報のチェック
            device_result = db.session.query(Device)\
                .filter(Device.user_hash == user_hash)\
                .filter(Device.device_id == device_id)\
                .first()
            
            if not device_result:
                msg = "device data is not found"
                return msg, 110

            # デバイスに紐づく記録データの削除
            db.session.query(SensorTemperature)\
                .filter(SensorTemperature.device_id == device_id)\
                .delete()
            
            db.session.commit()
            
        except sqlalchemy.exc.IntegrityError as exc:
            current_app.logger.critical("SQL Integrity error: %s" % exc)
            return None, 110
        except Exception as exc:
            current_app.logger.critical("Unknown error: %s" % exc)
            return None, 199

        msg = "ok"
        return msg, 0


