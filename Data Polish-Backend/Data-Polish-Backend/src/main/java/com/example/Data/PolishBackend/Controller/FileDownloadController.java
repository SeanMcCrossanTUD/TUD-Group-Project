package com.example.Data.PolishBackend.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import com.example.Data.PolishBackend.Service.FileDownloadService; // Import the FileUploadService


@RestController
@CrossOrigin(origins = {"http://16.170.150.247:9000", "http://localhost:4200"})
public class FileDownloadController {
    @Autowired
    private FileDownloadService fileDownloadService;

    @GetMapping("/download-csv")
    public ResponseEntity<String> downloadFile(@RequestParam String jobID) {
        // Call the service to get the file details as a JSON string
        return fileDownloadService.getFileDetails(jobID);
    }
}
