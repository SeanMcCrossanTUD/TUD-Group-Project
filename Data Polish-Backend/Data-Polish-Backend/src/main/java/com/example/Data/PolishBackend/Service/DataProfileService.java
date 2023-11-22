package com.example.Data.PolishBackend.Service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

/*
    take jobid as param
    query db with jobid to get dataprofileoutput value
    return it to frontend
 */
@Service
public class DataProfileService {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    public ResponseEntity<String> processDataProfile(String jobID) {
        try {
            // Retrieve 'dataprofileoutput' for the jobID from the database
            String sql = "SELECT dataprofileoutput FROM jobsandblobs WHERE jobid = ?";
            String dataProfile = jdbcTemplate.queryForObject(sql, String.class, jobID);

            if (dataProfile == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Data profile not found for jobID: " + jobID);
            }

            return ResponseEntity.ok(dataProfile);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}
