package com.example.Data.PolishBackend.Controller;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.http.ResponseEntity;
import com.example.Data.PolishBackend.Service.FileUploadService; // Import the FileUploadService

import java.io.IOException;
import java.util.Date;


@RestController
@CrossOrigin(origins = {"http://16.170.150.247:9000", "http://localhost:4200"})
public class FileUploadController {
    @Autowired
    private FileUploadService fileUploadService;

    // secure secret key 256 bits
    private final String secretKey = "WaaZ5eNs94mGk+joiqJf6Laj1s0oOrAyoy/saZJAaom801Rpqy88IaDZGhkhd65e";

    @PostMapping("/upload-csv")
    /*public ResponseEntity<String> uploadCSVFile(@RequestParam("file") MultipartFile file) throws IOException {
        return fileUploadService.uploadCSVFile(file);
    } */
    public ResponseEntity<String> uploadCSVFile(@RequestParam("file") MultipartFile file, @RequestHeader("Authorization") String token) throws IOException {

        // Validate the JWT token
        if (isValidJwtToken(token)) {
            return fileUploadService.uploadCSVFile(file);
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


