package com.example.Data.PolishBackend.Controller;

import com.example.Data.PolishBackend.Service.CleaningRulesExportService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class CleaningRulesExportController {
    @Autowired
    private CleaningRulesExportService cleaningRulesExportService;
    
    // secure secret key 256 bits
    private final String secretKey = "WaaZ5eNs94mGk+joiqJf6Laj1s0oOrAyoy/saZJAaom801Rpqy88IaDZGhkhd65e";

    @GetMapping("/rules-export")
    public ResponseEntity<String> exportCleaningRules(@RequestParam String jobID) {
        return cleaningRulesExportService.exportCleaningRules(jobID);
    }
}