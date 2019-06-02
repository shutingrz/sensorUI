create table device(
	device_id varchar(32) primary key,
	sensor_id integer,
	user_hash varchar(32),
	api_secret varchar(32)
);
