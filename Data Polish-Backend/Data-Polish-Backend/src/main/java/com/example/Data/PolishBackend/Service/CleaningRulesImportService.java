package com.example.Data.PolishBackend.Service;

import com.azure.storage.blob.BlobClient;
import com.azure.storage.blob.BlobContainerClient;
import com.azure.storage.blob.BlobServiceClient;
import com.azure.storage.blob.BlobServiceClientBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.UUID;
import java.io.IOException;

/*
* take jobid as param, json file (multipart file like upload) from frontend
* upload this json file into blob container 'rules', name of the blob? same as cleaning
* update db with the URI(this new file's name) in column 'cleaningrules'
* */

@Service
public class CleaningRulesImportService {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    //storing the blob connection string in a 'string' variable
    @Value("${azure.storage.connection-string}")
    private String azureConnectionString;


    public ResponseEntity<String> importCleaningRules(String jobID, MultipartFile jsonFile) {
        try {

            // Generate a unique filename for the JSON file
            String FileName = "rules_" + UUID.randomUUID() + ".json";

            // Store the JSON file to the 'rules' blob container
            storeJsonInBlobStorage(jsonFile, FileName);

            // Update the 'cleaningrules' column in the 'jobsandblobs' table
            String sql = "UPDATE jobsandblobs SET cleaningrules = ? WHERE jobid = ?";
            jdbcTemplate.update(sql, FileName, jobID);

            return ResponseEntity.status(HttpStatus.CREATED).build();
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error occurred during file upload: " + e.getMessage());
        }
    }

    //method to store json file in blob
    private void storeJsonInBlobStorage(MultipartFile jsonFile, String jsonFilename) {
        try {
            // Connect to Azure Blob Storage
            BlobContainerClient containerClient = new BlobServiceClientBuilder()
                    .connectionString(azureConnectionString)
                    .buildClient()
                    .getBlobContainerClient("rules");

            // Get a reference to the blob
            containerClient.getBlobClient(jsonFilename)
                    .upload(jsonFile.getInputStream(), jsonFile.getSize(), true);
        } catch (Exception e) {
            // Handle exceptions related to Azure Blob
            e.printStackTrace();
        }
    }
}

