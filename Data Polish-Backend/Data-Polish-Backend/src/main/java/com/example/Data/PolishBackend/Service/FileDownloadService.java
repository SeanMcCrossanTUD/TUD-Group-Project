package com.example.Data.PolishBackend.Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestParam;

@Service
public class FileDownloadService {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    public ResponseEntity<String> getFileDetails(String jobID) {
        String sql = "SELECT rawurl, dataprofileoutput, datacleaningoutput FROM jobsandblobs WHERE jobid = ?";
        try {
            // Execute the query to retrieve the file details
            String fileDetails = jdbcTemplate.queryForObject(sql, (rs, rowNum) -> {
                String rawurl = rs.getString("rawurl");
                String dataprofileoutput = rs.getString("dataprofileoutput");
                String datacleaningoutput = rs.getString("datacleaningoutput");
                return "{\"rawurl\":\"" + rawurl + "\", \"dataprofileoutput\":\"" + dataprofileoutput + "\", \"datacleaningoutput\":\"" + datacleaningoutput + "\"}";
            }, jobID);

            // Return the JSON response within a ResponseEntity
            return ResponseEntity.ok(fileDetails);
        } catch (Exception e) {
            // Handle exceptions, e.g., jobID not found, and return an appropriate error response
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Invalid Job ID");
        }
    }
}
