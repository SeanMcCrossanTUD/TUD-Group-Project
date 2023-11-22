package com.example.Data.PolishBackend.Controller;


import com.example.Data.PolishBackend.Service.DataProfileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;


@RestController
@CrossOrigin(origins = {"*"})
public class DataProfileController {
    @Autowired
    private DataProfileService dataProfileService;

    @GetMapping("/data-profile")
    public ResponseEntity<String> previewData(@RequestParam String jobID) {
        return dataProfileService.processDataProfile(jobID);
    }
}
