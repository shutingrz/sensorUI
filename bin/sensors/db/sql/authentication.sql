create table authentication(
	user_hash varchar(32) primary key,
	encrypted_password varchar(64) not null,
	hmac_key varchar(32) not null
);
