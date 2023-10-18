package com.example.Data.PolishBackend.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class DBCheckController {
    @Autowired
    private JdbcTemplate jdbcTemplate; // You can use JdbcTemplate for database queries

    @GetMapping("/check-db")
    public String checkDatabaseConnection() {
        try {
            jdbcTemplate.queryForObject("SELECT 1", Integer.class); // Execute a simple query
            return "Database connection is working!";
        } catch (Exception e) {
            return "Database connection error: " + e.getMessage();
        }
    }

}
