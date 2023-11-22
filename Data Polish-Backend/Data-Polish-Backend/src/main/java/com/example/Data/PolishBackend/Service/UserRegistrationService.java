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
            return new ResponseEntity<>("Invalid email address", HttpStatus.BAD_REQUEST);
        }

        // Check if the email already exists in the database
        if (emailExists(email)) {
            return new ResponseEntity<>("User already exists", HttpStatus.CONFLICT);
        }

        // Hash the password
        String hashedPassword = passwordEncoder.encode(password);

        // Insert user into the 'users' table
        String sql = "INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)";
        try {
            jdbcTemplate.update(sql, fullName, email, hashedPassword);
            return new ResponseEntity<>("New user successfully created", HttpStatus.CREATED);
        } catch (DataIntegrityViolationException e) {
            // Handle potential data integrity violation (e.g., unique constraint violation)
            return new ResponseEntity<>("User already exists", HttpStatus.CONFLICT);
        }
    }

    private boolean isValidEmail(String email) {
        // Add your email validation logic here (e.g., using regular expressions)
        // For simplicity, let's assume any non-null, non-empty email is valid in this example.
        return email != null && !email.isEmpty();
    }

    private boolean emailExists(String email) {
        // Check if the email already exists in the 'users' table
        String sql = "SELECT COUNT(*) FROM users WHERE email = ?";
        return jdbcTemplate.queryForObject(sql, Integer.class, email) > 0;
    }
}

