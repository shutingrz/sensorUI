
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DECIMAL, DATETIME, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
session = db.session
metadata = db.metadata
Model = db.Model


def init_db(app):
	db.init_app(app)
	Migrate(app, db)


def create_all():
	db.create_all()

	from app.db.orm.sensor_type import SensorType
	if db.session.query(SensorType).count() == 0:
			db.session.add(SensorType(
                sensor_id=1,
				sensor_name="Temperature"
			))
            
			db.session.commit()