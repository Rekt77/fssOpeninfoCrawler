create database fssRPA;
create table PDFS(
    id int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    date datetime,
    company varchar(20),
    reldept varchar(20),
    filename varchar(100),
    sha1 varchar(28));