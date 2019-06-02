from sensors import db

class SensorType(db.Model):
	def __init__(self, sensor_id, sensor_name):
			self.sensor_id = sensor_id
			self.sensor_name = sensor_name

db.mapper(SensorType, db.Table('sensor_type', db.metadata, autoload=True))
