package com.example.Data.PolishBackend.Controller;

import com.example.Data.PolishBackend.Service.CleaningRulesImportService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@RestController
public class CleaningRulesImportController {
    @Autowired
    private CleaningRulesImportService cleaningRulesImportService;

    // secure secret key 256 bits
    private final String secretKey = "WaaZ5eNs94mGk+joiqJf6Laj1s0oOrAyoy/saZJAaom801Rpqy88IaDZGhkhd65e";

    @PostMapping("/rules-import")
    public ResponseEntity<String> importCleaningRules(
            @RequestParam String jobID,
            @RequestParam("file") MultipartFile jsonFile,
            @RequestHeader("Authorization") String token
    ) throws IOException  {
        return cleaningRulesImportService.importCleaningRules(jobID, jsonFile);
    }
}