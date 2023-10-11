--create by Naveen Maheswaran
--sample query
-- insert into jobsandurl (rawfileurl,app1outputurl,app2outputurl)values('dsf','dsf','dsf') 
create table jobsandurl(
jobid raw(16) default sys_guid() primary key,
rawfileurl varchar(100) not null,
app1outputurl varchar(100),
app2outputurl varchar(100)
);

