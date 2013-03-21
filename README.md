qrround
=======

Personal test application
qrround


DotCloud
=======

dotcloud setup

dotcloud create djangotutorial
dotcloud push

dotcloud run db -- mysql
create database qrround;
create user 'qrround' identified by 'qrround';
grant all on qrround.* to 'qrround'@'%';

alter table qrround_userclient change friends friends longtext;

flush privileges;
exit;
