from sensors import db

class Device(db.Model):
	def __init__(self, device_id, sensor_id, user_hash, api_secret):
			self.device_id = device_id
			self.sensor_id = sensor_id
			self.user_hash = user_hash
			self.api_secret= api_secret

db.mapper(SensorType, db.Table('device', db.metadata, autoload=True))
