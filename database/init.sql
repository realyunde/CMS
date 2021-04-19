create user 'cms'@'%' identified by 'cms';
create database cms character set utf8;
grant all on cms.* to 'cms'@'%';
