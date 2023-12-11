package com.example.Data.PolishBackend.Service;

import com.azure.core.util.BinaryData;
import com.azure.messaging.servicebus.ServiceBusClientBuilder;
import com.azure.messaging.servicebus.ServiceBusMessage;
import com.azure.messaging.servicebus.ServiceBusSenderClient;
import com.sun.net.httpserver.HttpsParameters;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

import org.springframework.web.client.HttpStatusCodeException;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

/*
* take fullName, email from user
* create a random 4 digit OTP
* encrypt the OTP and store all these in DB
* send the unencrypted OTP, email to logic app
* return the 201 to frontend
* */
@Service
public class UserRegistrationService {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    //storing service connection string and queueName
    @Value("${azure.servicebus.connection-string}")
    private String serviceBusConnectionString;
    //@Value("${azure.servicebus.queue-name-q2}")
    @Value("${azure.servicebus.queue-name-mail}")
    private String queueName;
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
    private final String logicAppUrl = "https://prod-46.northeurope.logic.azure.com:443/workflows/643dcc1efa6a41908dd2846b226a0ffd/triggers/manual/paths/invoke";
    public ResponseEntity<String> registerUser(String fullName, String email) {
        // Generate a random 4-digit OTP
        String otp = generateRandomOTP();

        // Encrypt the OTP
        String encryptedOTP = passwordEncoder.encode(otp);

       /* // Validate email format
       if (!isValidEmail(email)) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Invalid email address");
        }*/

        // Check if the email already exists in the database
        if (emailExists(email)) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body("User already exists");
        }

        // Insert user into the 'users' table
        String sql = "INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)";
        try {
            jdbcTemplate.update(sql, fullName, email, encryptedOTP);

            // Send the unencrypted OTP and email to Logic App
            //sendToLogicApp(otp, email);

            //publish message to Azure Service Bus
           // publishMessageToQueue(jobID, dataResult.rawurl, dataResult.dataprofileoutput, jsonFileName);

            return ResponseEntity.status(HttpStatus.CREATED).body(otp);
        } catch (DataIntegrityViolationException e) {
            // Handle potential data integrity violation (e.g., unique constraint violation)
            return ResponseEntity.status(HttpStatus.CONFLICT).body("User already exists");
        }
    }

    private boolean isValidEmail(String email) {
        // Basic email format validation using a regular expression
        String emailRegex ="^(.+)@(\\S+) $";
                //"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$";

        // Check if the provided email matches the regular expression
        return email.matches(emailRegex);
    }

    private boolean emailExists(String email) {
        // Check if the email already exists in the 'users' table
        String sql = "SELECT COUNT(*) FROM users WHERE email = ?";
        return jdbcTemplate.queryForObject(sql, Integer.class, email) > 0;
    }

    private String generateRandomOTP() {
        // Generate a random 4-digit OTP
        Random random = new Random();
        int otp = 1000 + random.nextInt(9000);
        return String.valueOf(otp);
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

            // Close the sender and the ServiceBusClient
            senderClient.close();
        } catch (Exception e) {
            // Handle exceptions related to Azure Service Bus
            e.printStackTrace();
        }
    }

    private void sendToLogicApp(String otp, String email) {
        // Create a RestTemplate

        String url=logicAppUrl+"?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=9LE2z3sTd7ucTVWRYu2K-TuRPi1MT1pk_LLR5KSjIo8";
        RestTemplate restTemplate = new RestTemplate();

        // Set headers for the HTTP request
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);


        // Create a map for the request body
        Map<String, String> requestBody = new HashMap<>();
        requestBody.put("OTP", otp);
        requestBody.put("EMAILID", email);

        // Create a map for the query parameters
        Map<String, String> queryParams = new HashMap<>();
        queryParams.put("api-version", "2016-10-01"); // Add the api-version parameter

        // Create the HTTP entity with headers and body
        HttpEntity<Map<String, String>> requestEntity = new HttpEntity<>(requestBody, headers);

        // Make the HTTP POST request to the Logic App URL with query parameters
        try {
            ResponseEntity<String> responseEntity = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    requestEntity,
                    String.class

            );
        }catch (RestClientException e) {
            // Handle exceptions related to the REST client (e.g., network issues, timeout)
            e.printStackTrace();
        }
        /* Map<String, String> params = new HashMap<String, String>();
        params.put("api-version", "2016-10-01");
        params.put("sp", "%2Ftriggers%2Fmanual%2Frun");
        params.put("sv", "1.0");
        params.put("sig", "9LE2z3sTd7ucTVWRYu2K-TuRPi1MT1pk_LLR5KSjIo8");

        // Create the HTTP entity with headers and body
        HttpEntity<Map<String, String>> requestEntity = new HttpEntity<>(requestBody, headers);

        // Make the HTTP POST request to the Logic App URL
        //ResponseEntity<String> responseEntity = restTemplate.exchange(logicAppUrl, HttpMethod.POST, requestEntity, String.class);

        try {
            // Make the HTTP POST request to the Logic App URL
            ResponseEntity<String> responseEntity = restTemplate.exchange(logicAppUrl,HttpMethod.POST, requestEntity, String.class,params);


        } */
        /*// Handle the response if needed
        HttpStatus statusCode = responseEntity.getStatusCode();
        if (statusCode == HttpStatus.OK || statusCode == HttpStatus.CREATED) {
            System.out.println("Successfully sent to Logic App");
        } else {
            System.out.println("Failed to send to Logic App. Status code: " + statusCode);
        } */
    }
}

