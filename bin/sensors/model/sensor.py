import sqlalchemy
from sqlalchemy import or_
from flask import current_app
from sensors.util import Util
from sensors.model.ormutil import ORMUtil


class SensorModel(object):

	def __init__(self):
		pass

	def getSensorType(self):
		db = ORMUtil.initDB()
		SensorType = ORMUtil.getSensorTypeORM()

		if (db and SensorType) is None:
			return None, 100

		try:
			sensorType_result = db.session.query(SensorType).all()
		except Exception as exc:
			current_app.logger.critical("account_status: Unknown error: %s" % exc)
			return None, 199

		#sensorの対応表取得
		sensor_type = []
		for sensorType in sensorType_result:
			type_dict = {"id": sensorType.sensor_id, "name": sensorType.sensor_name}
			sensor_type.append(type_dict)

		return sensor_type, 0

