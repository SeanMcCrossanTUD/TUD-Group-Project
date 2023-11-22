package com.example.Data.PolishBackend.Service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserRegistrationService {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    public ResponseEntity<String> registerUser(String fullName, String email, String password) {
        // Validate email format
        if (!isValidEmail(email)) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Invalid email address");
        }

        // Check if the email already exists in the database
        if (emailExists(email)) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body("User already exists");
        }

        // Hash the password
        String hashedPassword = passwordEncoder.encode(password);

        // Insert user into the 'users' table
        String sql = "INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)";
        try {
            jdbcTemplate.update(sql, fullName, email, hashedPassword);
            return ResponseEntity.status(HttpStatus.CREATED).body("New user successfully created");
        } catch (DataIntegrityViolationException e) {
            // Handle potential data integrity violation (e.g., unique constraint violation)
            return ResponseEntity.status(HttpStatus.CONFLICT).body("User already exists");
        }
    }

    private boolean isValidEmail(String email) {
        // Basic email format validation using a regular expression
        String emailRegex = "^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$";

        // Check if the provided email matches the regular expression
        return email.matches(emailRegex);
    }

    private boolean emailExists(String email) {
        // Check if the email already exists in the 'users' table
        String sql = "SELECT COUNT(*) FROM users WHERE email = ?";
        return jdbcTemplate.queryForObject(sql, Integer.class, email) > 0;
    }
}

