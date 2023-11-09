package com.example.Data.PolishBackend.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import com.example.Data.PolishBackend.Service.DataCleaningService; // Import the DataCleaningService


@RestController
@CrossOrigin(origins = {"http://localhost:4200"})
public class DataCleaningController {
    @Autowired
    private DataCleaningService dataCleaningService;

    @GetMapping("/data-clean")
    public ResponseEntity<Void> cleanData(@RequestParam String jobID) {
        return dataCleaningService.processDataCleaning(jobID);
    }
}

