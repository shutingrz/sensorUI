create table sensor_temperature(
	id integer primary key autoincrement,
	device_id varchar(32) not null,
	time integer not null,
	temperature decimal not null,
	created_at timestamp not null default current_timestamp
);
