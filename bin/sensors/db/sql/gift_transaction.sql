create table gift_transaction(
	id bigint auto_increment primary key,
	sender varchar(32) not null, 
	receiver varchar(32) not null,
	value integer not null,
	message varchar(280),
	is_anonymous boolean,
	created_at timestamp not null default current_timestamp
);
