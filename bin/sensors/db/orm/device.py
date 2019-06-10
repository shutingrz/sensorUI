from sensors import db


class Device(db.Model):

    __tablename__ = "device"
    device_id = db.Column(db.String(32), primary_key=True)
    device_name = db.Column(db.String(255))
    sensor_type = db.Column(db.Integer, db.ForeignKey("sensor_type.sensor_id"))
    user_hash = db.Column(db.String(32), db.ForeignKey("user_hash.user_hash"))
    api_key = db.Column(db.String(32))

    userHash = db.relationship("UserHash")
    sensorType = db.relationship("SensorType")

    def __init__(self, device_id, device_name, sensor_type, user_hash, api_key):
        self.device_id = device_id
        self.device_name = device_name
        self.sensor_type = sensor_type
        self.user_hash = user_hash
        self.api_key = api_key


db.mapper(Device, db.Table('device', db.metadata, autoload=True))
