package com.example.Data.PolishBackend.Service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
/*
 * take jobid as param from frontend
 * query db with jobid and get value in column 'cleaningrules'
 * return the value
 * */
@Service
public class CleaningRulesExportService {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public ResponseEntity<String> exportCleaningRules(String jobID) {
        try {
            // Query the DB to get the cleaning rules for the specified jobID
            String sql = "SELECT cleaningrules FROM jobsandblobs WHERE jobid = ?";
            String cleaningRules = jdbcTemplate.queryForObject(sql, String.class, jobID);

            // Check if cleaningrules exists
            if (cleaningRules != null) {
                return ResponseEntity.ok(cleaningRules);
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Cleaning rules not found for the given jobID.");
            }

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error retrieving cleaning rules: " + e.getMessage());
        }
    }
}