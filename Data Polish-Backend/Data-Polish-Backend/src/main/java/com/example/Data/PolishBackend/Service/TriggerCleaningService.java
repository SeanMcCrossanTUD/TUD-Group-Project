package com.example.Data.PolishBackend.Service;

import com.azure.storage.blob.BlobClient;
import com.azure.storage.blob.BlobContainerClient;
import com.azure.storage.blob.BlobServiceClient;
import com.azure.storage.blob.BlobServiceClientBuilder;
import com.fasterxml.jackson.core.JsonProcessingException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import com.azure.messaging.servicebus.*;
import com.azure.core.util.BinaryData;
import org.springframework.stereotype.Service;
import com.fasterxml.jackson.databind.JsonNode; //Java doesn't have a built-in JSON object type, so need to use a library like Jackson to work with JSON objects.
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.UUID;

/*
* take jobID from frontend
* query DB with jobID and get file details - rawurl+dataprofileoutput+cleaningrules
* publish message with JobID and file details in queue 2
* */
@Service
public class TriggerCleaningService {
    //storing service connection string and queueName
    @Value("${azure.servicebus.connection-string}")
    private String serviceBusConnectionString;
    @Value("${azure.servicebus.queue-name-q2}")
    private String queueName;

    @Autowired
    private JdbcTemplate jdbcTemplate;

    //method for creating rawurl+dataprofileoutput+cleaningrules for the given jobID
    private static class DataResult {
        String rawurl;
        String dataprofileoutput;
        String cleaningrules;
    }
    public ResponseEntity<String> triggerCleaning(String jobID) {
        try {
            DataResult dataResult = new DataResult();


        }catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage());
        }

    }


}
