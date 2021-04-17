create user 'csms'@'%' identified by 'csms';
create database csms character set utf8;
grant all on csms.* to 'csms'@'%';
