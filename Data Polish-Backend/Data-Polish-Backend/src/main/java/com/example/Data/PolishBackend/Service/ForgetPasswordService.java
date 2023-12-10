package com.example.Data.PolishBackend.Service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Random;

/*
* take email from frontend
* generate a random 4 digit otp
* encode the otp and insert into 'users' table for the email
* return the unencrypted OTP
*  */

@Service
public class ForgetPasswordService {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    public ResponseEntity<String> forgetPassword(String email) {
        // Generate a random 4-digit OTP
        String otp = generateRandomOTP();

        // Encode the OTP
        String encodedOTP = passwordEncoder.encode(otp);

        // Insert the encoded OTP into the 'users' table for the given email
        String sql = "UPDATE users SET password = ? WHERE email = ?";
        try {
            jdbcTemplate.update(sql, encodedOTP, email);
            // Return the unencrypted OTP to the frontend
            return ResponseEntity.status(HttpStatus.OK).body(otp);
        } catch (DataIntegrityViolationException e) {
            // Handle potential data integrity violation (e.g., user not found)
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("User not found");
        }
    }

    //method to generate OTP
    private String generateRandomOTP() {
        // Generate a random 4-digit OTP
        Random random = new Random();
        int otp = 1000 + random.nextInt(9000);
        return String.valueOf(otp);
    }
}