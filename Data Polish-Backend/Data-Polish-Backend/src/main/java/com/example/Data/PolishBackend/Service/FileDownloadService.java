package com.example.Data.PolishBackend.Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestParam;

/*
    take jobid as param
    query db to get file details (every column)
    return file details in json format to frontend

    take jobid, fileType(excel,csv) as param
    query db with jobid to get 'datacleaningoutput' value and store it in string 'cleanedFile'
    download the blob (cleaned data) which name equals to 'cleanedFile'  from 'output' container
    check type of the file downloaded from container
    if file type matches with 'fileType' then return that file to frontend
    else convert the file to the 'fileType' and then return to frontend
 */
@Service
public class FileDownloadService {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    public ResponseEntity<String> downloadFile(String jobID,String fileType) {
        try {
            // Retrieve 'datacleaningoutput' from the database and store in cleanedFile
            String sql = "SELECT datacleaningoutput FROM jobsandblobs WHERE jobid = ?";
            String cleanedFile = jdbcTemplate.queryForObject(sql, String.class, jobID);

            if (cleanedFile == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(null);
            }





        /* prev code
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

         */
    }
}

