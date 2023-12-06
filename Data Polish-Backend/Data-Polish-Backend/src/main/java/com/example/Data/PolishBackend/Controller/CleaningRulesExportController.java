package com.example.Data.PolishBackend.Controller;

import com.example.Data.PolishBackend.Service.CleaningRulesExportService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class CleaningRulesExportController {
    @Autowired
    private CleaningRulesExportService cleaningRulesExportService;

    @GetMapping("/rules-export")
    public ResponseEntity<String> exportCleaningRules(@RequestParam String jobID) {
        return cleaningRulesExportService.exportCleaningRules(jobID);
    }
}