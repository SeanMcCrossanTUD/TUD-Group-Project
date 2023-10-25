use  datapolish

create table jobsandblobs(
jobid char(36) primary key,
rawurl varchar(100) not null,
dataprofileoutput varchar(100),
datacleaningoutput varchar(100)
);