package com.example.Data.PolishBackend.Service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;
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

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
    private final String logicAppUrl = "https://prod-46.northeurope.logic.azure.com:443/workflows/643dcc1efa6a41908dd2846b226a0ffd/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=snSWhGnz4e_yMCJKYJ0GFcKSUtVzAcb5iGrJ88hSSRo";

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
            sendToLogicApp(otp, email);
            return ResponseEntity.status(HttpStatus.CREATED).body("New user successfully created");
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

    private void sendToLogicApp(String otp, String email) {
        // Create a RestTemplate
        RestTemplate restTemplate = new RestTemplate();

        // Set headers for the HTTP request
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // Create a map for the request body
        Map<String, String> requestBody = new HashMap<>();
        requestBody.put("otp", otp);
        requestBody.put("email", email);

        // Create the HTTP entity with headers and body
        HttpEntity<Map<String, String>> requestEntity = new HttpEntity<>(requestBody, headers);

        // Make the HTTP POST request to the Logic App URL
        ResponseEntity<String> responseEntity = restTemplate.exchange(logicAppUrl, HttpMethod.POST, requestEntity, String.class);

        // Handle the response if needed
        HttpStatus statusCode = responseEntity.getStatusCode();
        if (statusCode == HttpStatus.OK || statusCode == HttpStatus.CREATED) {
            System.out.println("Successfully sent to Logic App");
        } else {
            System.out.println("Failed to send to Logic App. Status code: " + statusCode);
        }
    }
}

