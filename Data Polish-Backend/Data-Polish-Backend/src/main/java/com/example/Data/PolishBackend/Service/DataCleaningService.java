package com.example.Data.PolishBackend.Service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;

public class DataCleaningService {
    //data clean - get jobid from user then query db get dataprofilingoutput then put it in q2.
    @Autowired
    private JdbcTemplate jdbcTemplate;

    private class DataResult {
        String rawurl;
        String dataprofileoutput;
    }
    public ResponseEntity<String> processDataCleaning(String jobID) {
        try {
            DataResult dataResult = new DataResult();

            // Retrieve 'rawurl' and 'dataprofileoutput' from the database
            String sql = "SELECT rawurl, dataprofileoutput FROM jobsandblobs WHERE jobid = ?";

            jdbcTemplate.query(sql, new Object[]{jobID}, rs -> {
                dataResult.rawurl = rs.getString("rawurl");
                dataResult.dataprofileoutput = rs.getString("dataprofileoutput");
            });

            if (dataResult.rawurl == null || dataResult.dataprofileoutput == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Data not found for jobID: " + jobID);
            }

            // Construct JSON data
            String jsonData = "{\"jobID\":\"" + jobID + "\", \"rawurl\":\"" + dataResult.rawurl + "\", \"dataprofileoutput\":\"" + dataResult.dataprofileoutput + "\"}";

            // Store JSON data in Azure Service Bus 'q2' (add your Azure Service Bus logic here)

            // Return a success response
            return ResponseEntity.ok("Data stored in Azure Service Bus 'q2': " + jsonData);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error processing data: " + e.getMessage());
        }
    }
}
