create table profile(
	user_id varchar(64) primary key,
	nickname varchar(16),
	icon_path varchar(64),
	email varchar(256),
  department varchar(64),
	introduction varchar(3000)
) character set utf8mb4;
