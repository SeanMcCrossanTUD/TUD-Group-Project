DELIMITER //
CREATE PROCEDURE getjobid(IN rawurl varchar(100))
begin
		declare guid char(36);
		set guid=uuid();
        insert into jobsandblobs(jobid,rawurl) values(guid,rawurl);
        
        select guid;
        end;
 //

DELIMITER ;

--call getjobid('abc');