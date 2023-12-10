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

            // Decode the 'encodedOTP' value
            String decodedOTP = passwordEncoder.decode(encodedOTP);
            if (decodedOTP.equals(otp)) {
                // Hash the new password
                String hashedPassword = passwordEncoder.encode(newPassword);

            }
}
