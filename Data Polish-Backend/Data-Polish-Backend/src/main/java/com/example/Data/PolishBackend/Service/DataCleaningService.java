package com.example.Data.PolishBackend.Service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import com.azure.messaging.servicebus.*;
import com.azure.core.util.BinaryData;
import org.springframework.stereotype.Service;

@Service
public class DataCleaningService {
    //data clean - get jobid from user then query db get dataprofilingoutput then put it in q2.

    //storing service connection string and queueName
    @Value("${azure.servicebus.connection-string}")
    private String serviceBusConnectionString;
    @Value("${azure.servicebus.queue-name-q2}")
    private String queueName;
    @Autowired
    private JdbcTemplate jdbcTemplate;


    private static class DataResult {
        String rawurl;
        String dataprofileoutput;
    }
    public ResponseEntity<Void> processDataCleaning(String jobID) {
        try {
            DataResult dataResult = new DataResult();

            // Retrieve 'rawurl' and 'dataprofileoutput' from the database
            String sql = "SELECT rawurl, dataprofileoutput FROM jobsandblobs WHERE jobid = ?";

            jdbcTemplate.query(sql, new Object[]{jobID}, rs -> {
                dataResult.rawurl = rs.getString("rawurl");
                dataResult.dataprofileoutput = rs.getString("dataprofileoutput");
            });

            if (dataResult.rawurl == null || dataResult.dataprofileoutput == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
            }

            // Connect to Azure Service Bus
            ServiceBusSenderClient senderClient = new ServiceBusClientBuilder()
                    .connectionString(serviceBusConnectionString)
                    .sender()
                    .queueName(queueName)
                    .buildClient();

            // Construct the JSON message to send
            String jsonData = "{\"jobID\":\"" + jobID + "\", \"rawurl\":\"" + dataResult.rawurl + "\", \"dataprofileoutput\":\"" + dataResult.dataprofileoutput + "\"}";

            // Convert the JSON to BinaryData
            BinaryData messageData = BinaryData.fromString(jsonData);

            // Create a ServiceBusMessage with the JSON data
            ServiceBusMessage message = new ServiceBusMessage(messageData);

            // Send the message to the 'q2' queue
            senderClient.sendMessage(message);

            // Close the sender and the ServiceBusClient when done
            senderClient.close();

            // Return a success response with no body
            return ResponseEntity.status(HttpStatus.CREATED).build();
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}
