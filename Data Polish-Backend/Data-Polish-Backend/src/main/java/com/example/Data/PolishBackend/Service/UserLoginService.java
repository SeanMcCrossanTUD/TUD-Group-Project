package com.example.Data.PolishBackend.Service;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Date;

@Service
public class UserLoginService {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
    private final String secretKey = "mySecretKey"; // secure secret key

    public ResponseEntity<String> loginUser(String email, String password) {
        // Check if the email exists in the 'users' table
        if (!emailExists(email)) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("User doesn't exist");
        }

        // Get the hashed password from the 'users' table
        String hashedPassword = getHashedPasswordByEmail(email);

        // Check if the entered password matches the hashed password
        if (!passwordEncoder.matches(password, hashedPassword)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Incorrect password");
        }

        // Generate JWT token
        String token = generateJwtToken(email);

        // You can customize the response based on your needs
        return ResponseEntity.status(HttpStatus.OK).body("Login successful. Token: " + token);
    }

    private boolean emailExists(String email) {
        // Check if the email exists in the 'users' table
        String sql = "SELECT COUNT(*) FROM users WHERE email = ?";
        return jdbcTemplate.queryForObject(sql, Integer.class, email) > 0;
    }

    private String getHashedPasswordByEmail(String email) {
        // Retrieve the hashed password from the 'users' table
        String sql = "SELECT password FROM users WHERE email = ?";
        return jdbcTemplate.queryForObject(sql, String.class, email);
    }

    private String generateJwtToken(String email) {
        // Generate a simple JWT token with the email as the subject
        return Jwts.builder()
                .setSubject(email)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + 86400000)) // 1 day expiration
                .signWith(SignatureAlgorithm.HS256, secretKey)
                .compact();
    }
}
