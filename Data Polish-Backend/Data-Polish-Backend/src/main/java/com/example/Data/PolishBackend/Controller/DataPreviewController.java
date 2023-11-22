package com.example.Data.PolishBackend.Controller;

import com.example.Data.PolishBackend.Service.DataCleaningService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import com.example.Data.PolishBackend.Service.DataPreviewService; // Import the DataCleaningService

@RestController
@CrossOrigin(origins = {"*"})
public class DataPreviewController {
    @Autowired
    private DataPreviewService dataPreviewService;

    @GetMapping("/data-preview")
    public ResponseEntity<String> previewData(@RequestParam String jobID) {
        return dataPreviewService.processDataPreview(jobID);
    }
}
