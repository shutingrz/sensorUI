from sensors import db

class SensorTemperature(db.Model):
	def __init__(self, device_id, time, temperature):
			self.device_id = device_id
			self.time = time
			self.temperature = temperature

db.mapper(SensorType, db.Table('sensor_temperature', db.metadata, autoload=True))
