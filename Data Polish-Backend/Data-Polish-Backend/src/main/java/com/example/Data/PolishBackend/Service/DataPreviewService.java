package com.example.Data.PolishBackend.Service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import com.azure.messaging.servicebus.*;
import com.azure.core.util.BinaryData;
import org.springframework.stereotype.Service;

/*
    take jobid as param
    query db with jobid to get datapreview entry
    return it to frontend
 */
@Service
public class DataPreviewService {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    public ResponseEntity<String> processDataPreview(String jobID) {
        try {
            // Retrieve 'datapreview' for the jobID from the database
            String sql = "SELECT datapreview FROM jobsandblobs WHERE jobid = ?";
            String dataPreview = jdbcTemplate.queryForObject(sql, String.class, jobID);

            if (dataPreview == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Data preview not found for jobID: " + jobID);
            }

            return ResponseEntity.ok(dataPreview);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}
