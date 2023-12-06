package com.example.Data.PolishBackend.Controller;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.example.Data.PolishBackend.Service.FileDownloadService; // Import the FileUploadService

import java.io.File;
import java.util.Date;


@RestController
//@CrossOrigin(origins = {"http://16.170.150.247:9000", "http://localhost:4200"})
public class FileDownloadController {
    @Autowired
    private FileDownloadService fileDownloadService;

    // secure secret key 256 bits
    private final String secretKey = "WaaZ5eNs94mGk+joiqJf6Laj1s0oOrAyoy/saZJAaom801Rpqy88IaDZGhkhd65e";

    @GetMapping("/download-file")
    /*public ResponseEntity<String> downloadFile(@RequestParam String jobID) {
        // Call the service to get the file details as a JSON string
        return fileDownloadService.getFileDetails(jobID);
    } */
    public ResponseEntity<Resource> downloadFile(
            @RequestParam String jobID,
            @RequestParam String fileType,
            @RequestHeader("Authorization") String token)
    {
        // Validate the JWT token
        if (isValidJwtToken(token)) {
            return fileDownloadService.downloadFile(jobID,fileType);
        } else {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body((Resource) new File("Unauthorized access"));
            //return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Unauthorized access".getBytes());
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
