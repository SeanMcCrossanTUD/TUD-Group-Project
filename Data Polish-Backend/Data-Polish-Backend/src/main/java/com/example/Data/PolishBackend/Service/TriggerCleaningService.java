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

            // Retrieve 'rawurl','dataprofileoutput' and 'cleaningrules' from the database
            String sql = "SELECT rawurl, dataprofileoutput, cleaningrules FROM jobsandblobs WHERE jobid = ?";

            jdbcTemplate.query(sql, new Object[]{jobID}, rs -> {
                dataResult.rawurl = rs.getString("rawurl");
                dataResult.dataprofileoutput = rs.getString("dataprofileoutput");
                dataResult.cleaningrules = rs.getString("cleaningrules");
            });

            //check if value not found in DB
            if (dataResult.rawurl == null || dataResult.dataprofileoutput == null || dataResult.cleaningrules == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("File not found for the job id.");
            }

            //publish message to Azure Service Bus
            publishMessageToQueue(jobID, dataResult.rawurl, dataResult.dataprofileoutput, dataResult.cleaningrules);

            // Return a success response with no body
            return ResponseEntity.status(HttpStatus.CREATED).build();
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage());
        }

    }

    //method to publish message to Azure Service Bus
    private void publishMessageToQueue(String jobID, String rawurl, String dataprofileoutput, String cleaningrules) {
        try {
            // Connect to Azure Service Bus
            ServiceBusSenderClient senderClient = new ServiceBusClientBuilder()
                    .connectionString(serviceBusConnectionString)
                    .sender()
                    .queueName(queueName)
                    .buildClient();

            // Construct the JSON message to send
            String jsonData = "{\"jobID\":\"" + jobID + "\"," +
                    " \"rawurl\":\"" + rawurl + "\", " +
                    "\"dataprofileoutput\":\"" + dataprofileoutput + "\", " +
                    "\"cleaningrules\":\"" + cleaningrules + "\"}";

            // Convert the JSON to BinaryData
            BinaryData messageData = BinaryData.fromString(jsonData);

            // Create a ServiceBusMessage with the JSON data
            ServiceBusMessage message = new ServiceBusMessage(messageData);

            // Send the message to the 'q2' queue
            senderClient.sendMessage(message);

            // Close the sender and the ServiceBusClient
            senderClient.close();
        } catch (Exception e) {
            // Handle exceptions related to Azure Service Bus
            e.printStackTrace();
        }
    }
}
