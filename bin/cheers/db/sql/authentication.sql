create table authentication(
	user_id varchar(64) primary key,
	encrypted_password varchar(64) not null,
	hmac_key varchar(32) not null
);
