from sensors import db
from datetime import datetime


class SensorTemperature(db.Model):

    __tablename__ = "sensor_temperature"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    device_id = db.Column(db.String(32), db.ForeignKey("device.device_id"), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Integer, nullable=True)
    created = db.Column(db.DATETIME, default=datetime.now, nullable=False)

    def __init__(self, device_id, time, temperature):
        self.device_id = device_id
        self.time = time
        self.temperature = temperature
