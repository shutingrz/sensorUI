from flask import current_app
from sensors.util import Util
from sensors.model.ormutil import ORMUtil
import sqlalchemy

class AccountModel(object):

    def __init__(self):
        pass

    def account_status(self, user_hash):
        db = ORMUtil.initDB()
        User = ORMUtil.getUserORM()
        Device = ORMUtil.getDeviceORM()
        SensorType = ORMUtil.getSensorTypeORM()


        if (db and User and Device and SensorType) is None:
            return None, 100

        try:
            device_result = db.session.query(Device).filter(Device.user_hash == user_hash).all()
            sensorType_result = db.session.query(SensorType).all()
        except Exception as exc:
            current_app.logger.critical("account_status: Unknown error: %s" % exc)
            return None, 199

        #sensorの対応表取得
        sensor_type = []
        for sensorType in sensorType_result:
            type_dict = {"id": sensorType.sensor_id, "name": sensorType.sensor_name}
            sensor_type.append(type_dict)

        devices = []
        
        for device in device_result:
            device_dict = { "device_name": device.device_name,
                            "device_id": device.device_id,
                            "sensor_type": device.sensor_type,
                            "api_key": device.api_key}
            
            devices.append(device_dict)

            
        msg = {"devices": devices}

        return msg, 0

    def device_register(self, user_hash, device_name, sensor_type):
        db = ORMUtil.initDB()
        Device = ORMUtil.getDeviceORM()
        SensorType = ORMUtil.getSensorTypeORM()

        if (db and Device and SensorType) is None:
            return None, 100

        device_id = Util.generateRandomString(32)
        api_key = Util.generateRandomString(32)

        try:
            db.session.add(Device(
                device_id=device_id,
                device_name=device_name,
                sensor_type=sensor_type,
                user_hash=user_hash,
                api_key=api_key))
            
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as exc:
            current_app.logger.critical("SQL Integrity error: %s" % exc)
            return None, 110
        except Exception as exc:
            current_app.logger.critical("Unknown error: %s" % exc)
            return None, 199
        
        device_dict = { "device_name": device_name,
                        "device_id": device_id,
                        "sensor_type": sensor_type,
                        "api_key": api_key}

        return device_dict, 0



        

