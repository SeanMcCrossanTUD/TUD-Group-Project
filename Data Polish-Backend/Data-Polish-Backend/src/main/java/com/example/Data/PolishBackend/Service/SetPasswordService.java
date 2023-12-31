package com.example.Data.PolishBackend.Service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

/*
* take strings email, otp, password from frontend
* get value from 'password' column from 'users' table for the email and store it as string 'encodedOTP'
* decode the 'encodedOTP' value and match with otp from frontend
* if they match then hash the password taken from frontend and insert hashed password into 'password' column
* else return "OTP is invalid"
* */

@Service
public class SetPasswordService {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    public ResponseEntity<String> setPassword(String email, String otp, String newPassword) {
        try {
            // Retrieve the 'encodedOTP' from the 'users' table for the given email
            String encodedOTP = jdbcTemplate.queryForObject(
                    "SELECT password FROM users WHERE email = ?",
                    String.class,
                    email
            );

            // Check if the raw OTP matches the encoded password
            if (passwordEncoder.matches(otp, encodedOTP)) {
                // Hash the new password
                String hashedPassword = passwordEncoder.encode(newPassword);

                // Update the 'password' column with the new hashed password
                jdbcTemplate.update("UPDATE users SET password = ? WHERE email = ?", hashedPassword, email);

                return ResponseEntity.status(HttpStatus.OK).body("Password successfully updated");
            } else {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("OTP is invalid");
            }
        } catch (EmptyResultDataAccessException e) {
            // Handle the case where the email is not found in the 'users' table
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("User not found");
        } catch (Exception e) {
            // Handle other exceptions
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage());
        }
    }
}
