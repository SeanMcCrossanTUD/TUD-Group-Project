package com.example.Data.PolishBackend.Service;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.HashSet;
import java.util.Set;

@Service
public class UserLogoutService {
    private final Set<String> tokenBlacklist = new HashSet<>();

    public ResponseEntity<String> logoutUser(String token) {
        try {
            // Add the token to the blacklist
            addToBlacklist(token);
            return ResponseEntity.status(HttpStatus.OK).body("Successfully logged out.");
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error during logout");
        }
    }

    private void addToBlacklist(String token) {
        // Add the token to the blacklist set
        tokenBlacklist.add(token);
    }

    public boolean isTokenBlacklisted(String token) {
        // Check if the token is in the blacklist
        return tokenBlacklist.contains(token);
    }
}