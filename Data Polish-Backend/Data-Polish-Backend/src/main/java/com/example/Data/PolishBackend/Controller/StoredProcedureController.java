package com.example.Data.PolishBackend.Controller;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.dao.DataAccessException;

import java.io.IOException;


@Controller
public class StoredProcedureController {
    @Autowired
    private JdbcTemplate jdbcTemplate; // You can use JdbcTemplate for database queries

    @GetMapping("/callStoredProcedure")
    public String callStoredProcedure() throws IOException {
        String filename = "aaa";
        /*try {
            filename = "aaa";
            String sql = "CALL getjobid(?)";
            //jdbcTemplate.execute("call getjobid('last')");
            jdbcTemplate.update(sql, filename);


        } catch (DataAccessException e) {
            return "An error occurred during the file upload: " + e.getMessage();
        } catch (Exception e) {
            return "An error occurred: " + e.getMessage();
        } */
        try {
            //call stored procedure and get jobid
            String sql2 = "SELECT jobid FROM jobsandblobs WHERE rawurl = ?";
            String jobId = jdbcTemplate.queryForObject(sql2,String.class,filename);
            return jobId;
        }
        catch (Exception e) {
            return "error"+e.getMessage();
        }

    }
}

