ALTER ROLE web_db_user WITH SUPERUSER PASSWORD 'web_db_password1234';
ALTER DATABASE web_db OWNER TO web_db_user;
-- CREATE DATABASE web_db WITH OWNER = 'web_db_user';