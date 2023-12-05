package com.example.Data.PolishBackend.Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestParam;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
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

    public ResponseEntity<Resource> downloadFile(String jobID, String fileType) {
        try {
            // Retrieve 'datacleaningoutput' from the database and store in cleanedFile
            String sql = "SELECT datacleaningoutput FROM jobsandblobs WHERE jobid = ?";
            String cleanedFile = jdbcTemplate.queryForObject(sql, String.class, jobID);

            if (cleanedFile == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(null);
            }

            // Construct the URL for downloading the file from Azure Blob Storage
            String blobUrl = String.format("https://fab5storage.blob.core.windows.net/output/%s", cleanedFile);

            // Download the file using HTTP
            byte[] fileContent = downloadBlob(blobUrl);

            // Extract file extension from cleanedFile
            String fileExtension = cleanedFile.substring(cleanedFile.lastIndexOf('.'));

            // If the file extension matches the requested fileType, return the file
            if (fileExtension.equals(fileType)) {
                ByteArrayResource resource = new ByteArrayResource(fileContent);
                return ResponseEntity.ok()
                        .header("Content-Disposition", "attachment;filename=" + cleanedFile)
                        .body(resource);
            } else {
                // Convert the file to the requested fileType
                byte[] convertedFileContent;
                if (fileType.equals(".csv")) {
                    // Implement CSV to XLSX conversion logic
                    convertedFileContent = convertCsvToXlsx(fileContent);
                } else if (fileType.equals(".xlsx")) {
                    // Implement XLSX to CSV conversion logic
                    convertedFileContent = convertXlsxToCsv(fileContent);
                } else {
                    return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(null);
                }

                String convertedFileName = cleanedFile.replace(fileExtension, fileType);
                ByteArrayResource resource = new ByteArrayResource(convertedFileContent);
                return ResponseEntity.ok()
                        .header("Content-Disposition", "attachment;filename=" + convertedFileName)
                        .body(resource);
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
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
    private byte[] downloadBlob(String blobUrl) throws IOException {
        try {
            URL url = new URL(blobUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            try (InputStream inputStream = connection.getInputStream()) {
                return inputStream.readAllBytes();
            }
        } catch (IOException e) {
            throw e;
        }
    }
}

