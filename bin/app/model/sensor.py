import sqlalchemy
from flask import current_app

from app.util import ResultCode
from app import db
from app.db.orm import SensorType


class SensorModel(object):

	def __init__(self):
		pass

	def getSensorType(self):

		try:
			sensorType_result = db.session.query(SensorType).all()
		except Exception as exc:
			current_app.logger.critical("getSensorType: Unknown error: %s" % exc)
			return None, ResultCode.DBError

		#sensorの対応表取得
		sensor_type = []
		for sensorType in sensorType_result:
			type_dict = {"id": sensorType.sensor_id, "name": sensorType.sensor_name}
			sensor_type.append(type_dict)

		return sensor_type, ResultCode.Success

