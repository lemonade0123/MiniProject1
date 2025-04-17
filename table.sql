create database news_db;
use news_db;

ALTER DATABASE news_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;



create table word_list (
	id bigint not null primary key auto_increment,
	append_word varchar(255) not null,
	append_date varchar(10) not null,
	append_count int default 0
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


