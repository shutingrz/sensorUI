from sensors import db


class Device(db.Model):

    __tablename__ = "device"
    device_id = db.Column(db.String(32), primary_key=True)
    sensor_type = db.Column(db.Integer, db.ForeignKey("sensor_type.sensor_id"))
    user_hash = db.Column(db.String(32), db.ForeignKey("user_hash.user_hash"))
    api_secret = db.Column(db.String(32))

    userHash = db.relationship("UserHash")
    sensorType = db.relationship("SensorType")

    def __init__(self, device_id, sensor_type, user_hash, api_secret):
        self.device_id = device_id
        self.sensor_type = sensor_type
        self.user_hash = user_hash
        self.api_secret = api_secret


db.mapper(Device, db.Table('device', db.metadata, autoload=True))
