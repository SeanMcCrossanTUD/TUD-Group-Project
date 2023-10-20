package com.example.Data.PolishBackend.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;



@RestController
public class DBCheckController {
    @Autowired
    private JdbcTemplate jdbcTemplate; // You can use JdbcTemplate for database queries

    @GetMapping("/check-db")
    public String checkDatabaseConnection() {
        try {

            //perfect one is the below one
            //String jobid = jdbcTemplate.queryForObject("call getjobid('bbb')",String.class);

            //  jdbcTemplate.queryForObject("SELECT 1", Integer.class); // Execute a simple query
           // return "Database connection is working!";
            String filename = "c";
            String sql = "CALL getjobid(?)"; // Adjust the SQL query as needed
            String result = jdbcTemplate.queryForObject(sql,String.class,filename);

            return result;

            //String sql = "call getjobid('new1')";
            //jdbcTemplate.execute(sql);
            //return "ok";
        } catch (Exception e) {
            return "Database connection error: " + e.getMessage();
        }
    }

}


