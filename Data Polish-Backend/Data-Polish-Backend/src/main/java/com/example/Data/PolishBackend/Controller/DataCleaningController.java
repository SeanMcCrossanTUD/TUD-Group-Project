package com.example.Data.PolishBackend.Controller;

import com.fasterxml.jackson.databind.JsonNode;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.example.Data.PolishBackend.Service.DataCleaningService; // Import the DataCleaningService

import java.util.Date;


@RestController
@CrossOrigin(origins = {"http://16.170.150.247:9000", "http://localhost:4200"})
public class DataCleaningController {
    @Autowired
    private DataCleaningService dataCleaningService;

    // secure secret key 256 bits
    private final String secretKey = "WaaZ5eNs94mGk+joiqJf6Laj1s0oOrAyoy/saZJAaom801Rpqy88IaDZGhkhd65e";

    @PostMapping("/data-clean")
    /*public ResponseEntity<String> cleanData(@RequestParam String jobID, @RequestBody JsonNode cleaningRules) {
        return dataCleaningService.processDataCleaning(jobID,cleaningRules);
    }*/
    public ResponseEntity<String> cleanData(@RequestParam String jobID, @RequestBody JsonNode cleaningRules, @RequestHeader("Authorization") String token) {

        // Validate the JWT token
        if (isValidJwtToken(token)) {
            return dataCleaningService.processDataCleaning(jobID,cleaningRules);
        } else {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Unauthorized access");
        }
    }



    private boolean isValidJwtToken(String token) {
        try {
            // Remove the "Bearer " prefix if present
            if (token.startsWith("Bearer ")) {
                token = token.substring(7);
            }
            // Parse the token and extract claims
            Claims claims = Jwts.parser().setSigningKey(secretKey).parseClaimsJws(token).getBody();

            // Log the claims for debugging
            System.out.println("Token Claims: " + claims);

            // Check if the token has expired
            if (claims.getExpiration() != null && claims.getExpiration().before(new Date())) {
                // Token has expired
                System.out.println("Token has expired");
                return false;
            }

            // If no exception is thrown, the token is valid
            return true;
        } catch (Exception e) {
            // An exception is thrown if the token is invalid
            System.out.println("Exception during token validation: " + e.getMessage());
            return false;
        }
    }
}

