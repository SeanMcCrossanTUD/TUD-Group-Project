package com.example.Data.PolishBackend.Controller;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.example.Data.PolishBackend.Service.DataCleaningService; // Import the DataCleaningService


@RestController
@CrossOrigin(origins = {"http://localhost:4200"})
public class DataCleaningController {
    @Autowired
    private DataCleaningService dataCleaningService;

    @GetMapping("/data-clean")
    public ResponseEntity<String> cleanData(@RequestParam String jobID, @RequestBody JsonNode cleaningRules) {
        return dataCleaningService.processDataCleaning(jobID,cleaningRules);
    }
}

