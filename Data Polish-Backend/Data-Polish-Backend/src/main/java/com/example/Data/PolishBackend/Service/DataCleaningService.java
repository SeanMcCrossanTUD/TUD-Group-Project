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
    v1:
    data clean - get jobid from user then query db get dataprofilingoutput
    put it in q2.

    v2:
    take jobid and json object from frontend
    query db with jobid to get dataprofilingoutput value

    convert the json object to json file
    create json filename rules+uuid.json //uuid to make each file unique
    store the json filename in DB under cleaningrules column for that jobid
    store the json file in blob - rules

    publish to q2
        - retrieved dataprofilingoutput value (to trigger datacleaning py microservice)
        - json filename

 */
@Service
public class DataCleaningService {

    //storing service connection string and queueName
    @Value("${azure.servicebus.connection-string}")
    private String serviceBusConnectionString;
    @Value("${azure.servicebus.queue-name-q2}")
    private String queueName;

    //storing the blob connection string in a 'string' variable
    @Value("${azure.storage.connection-string}")
    private String azureConnectionString;
    @Autowired
    private JdbcTemplate jdbcTemplate;


    //method for creating rawurl+dataprofileoutput for the given jobID
    private static class DataResult {
        String rawurl;
        String dataprofileoutput;
    }

    //method to save a JSON object to a JSON file
    private String convertToJsonFile(JsonNode jsonNode, String rawurl) throws IOException, JsonProcessingException {
        // Generate a unique filename based on the 'rawurl' and a random UUID
        String fileName = "rules_" + UUID.randomUUID() + ".json";

        // Create an ObjectMapper to convert the JSON object to bytes
        ObjectMapper objectMapper = new ObjectMapper();

        // Write the JSON bytes to a file with the generated filename
        //Files.write(new File(fileName).toPath(), objectMapper.writeValueAsBytes(jsonNode));
        File jsonFile = new File(fileName);
        objectMapper.writeValue(jsonFile, jsonNode);
        return fileName;
    }

    //method to store JSON file in blob
    private void storeJsonInBlobStorage(String jsonFilename) {
        try {
            // Connect to Azure Blob Storage
            BlobServiceClient blobServiceClient = new BlobServiceClientBuilder()
                    .connectionString(azureConnectionString)
                    .buildClient();

            // Get a reference to the container
            BlobContainerClient containerClient = blobServiceClient.getBlobContainerClient("rules");

            // Get a reference to the blob
            BlobClient blobClient = containerClient.getBlobClient(jsonFilename);

            // Upload the file to Azure Blob Storage
            blobClient.uploadFromFile(jsonFilename, true);
        } catch (Exception e) {
            // Handle exceptions related to Azure Blob
            e.printStackTrace();
        }
    }

    //method to publish message to Azure Service Bus
    private void publishMessageToQueue(String jobID, String rawurl, String dataprofileoutput, String jsonFilename) {
        try {
            // Connect to Azure Service Bus
            ServiceBusSenderClient senderClient = new ServiceBusClientBuilder()
                    .connectionString(serviceBusConnectionString)
                    .sender()
                    .queueName(queueName)
                    .buildClient();

            // Construct the JSON message to send
            String jsonData = "{\"jobID\":\"" + jobID + "\", \"rawurl\":\"" + rawurl + "\", \"dataprofileoutput\":\"" + dataprofileoutput + "\", \"jsonFilename\":\"" + jsonFilename + "\"}";

            // Convert the JSON to BinaryData
            BinaryData messageData = BinaryData.fromString(jsonData);

            // Create a ServiceBusMessage with the JSON data
            ServiceBusMessage message = new ServiceBusMessage(messageData);

            // Send the message to the 'q2' queue
            senderClient.sendMessage(message);

            // Close the sender and the ServiceBusClient when done
            senderClient.close();
        } catch (Exception e) {
            // Handle exceptions related to Azure Service Bus
            e.printStackTrace();
        }
    }

    public ResponseEntity<String> processDataCleaning(String jobID,JsonNode cleaningRules) {
        try {
            DataResult dataResult = new DataResult();

            // Retrieve 'rawurl' and 'dataprofileoutput' from the database
            String sql = "SELECT rawurl, dataprofileoutput FROM jobsandblobs WHERE jobid = ?";

            jdbcTemplate.query(sql, new Object[]{jobID}, rs -> {
                dataResult.rawurl = rs.getString("rawurl");
                dataResult.dataprofileoutput = rs.getString("dataprofileoutput");
            });

            if (dataResult.rawurl == null || dataResult.dataprofileoutput == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("File not found for the job id.");
            }

            // Convert JSON object to a JSON file and create the json filename
            String jsonFileName = convertToJsonFile(cleaningRules, dataResult.rawurl);

            // Store the JSON filename in the database
            String updateSql = "UPDATE jobsandblobs SET cleaningrules = ? WHERE jobid = ?";
            jdbcTemplate.update(updateSql, jsonFileName, jobID);

            // Store the JSON file in Azure Blob Storage
            storeJsonInBlobStorage(jsonFileName);

            //publish message to Azure Service Bus
            publishMessageToQueue(jobID, dataResult.rawurl, dataResult.dataprofileoutput, jsonFileName);

            // Return a success response with no body
            return ResponseEntity.status(HttpStatus.CREATED).build();
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}
