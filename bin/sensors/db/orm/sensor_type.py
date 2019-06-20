from sensors import db

class SensorType(db.Model):

    __tablename__ = "sensor_type"
    sensor_id = db.Column(db.Integer, primary_key=True)
    sensor_name = db.Column(db.String(32), nullable=False)

    def __init__(self, sensor_id, sensor_name):
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name

