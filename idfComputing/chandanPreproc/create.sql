-- create.sql

-- creates the tweet table for twitter data
-- contains the first 3 columns - tweet ID, date and time, content

drop table if exists tweet_en;

create table tweet_en ( 
	id BIGINT(20) UNSIGNED, 
	creation_date DATETIME,
	content VARCHAR(150) 
	);