from sensors import db

class SensorTemperature(db.Model):

	__tablename__ = "sensor_temperature"
	id = db.Column(db.Integer(unsigned=True), primary_key=True, autoincrement=True)
	device_id = db.Column(db.String(32), db.ForeignKey("device.device_id"))
	time = db.Column(db.Integer, nullable=False)
	temperature = db.Column(db.DECIMAL, nullable=True)
	created = db.Column(db.DATETIME, default=datetime.now, nullable=False)

	device = db.relationship("Device")

	def __init__(self, device_id, time, temperature):
			self.device_id = device_id
			self.time = time
			self.temperature = temperature

db.mapper(SensorType, db.Table('sensor_temperature', db.metadata, autoload=True))
