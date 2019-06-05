create table device(
	device_name varchar(64) not null,
	device_id varchar(32) primary key,
	sensor_id integer not null,
	user_hash varchar(32) not null,
	apikey varchar(32) not null
);
