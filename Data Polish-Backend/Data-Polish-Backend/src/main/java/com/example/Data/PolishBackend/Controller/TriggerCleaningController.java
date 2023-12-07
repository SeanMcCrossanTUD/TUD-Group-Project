package com.example.Data.PolishBackend.Controller;

import com.example.Data.PolishBackend.Service.TriggerCleaningService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class TriggerCleaningController {

    private TriggerCleaningService triggerCleaningService;

    // secure secret key 256 bits
    private final String secretKey = "WaaZ5eNs94mGk+joiqJf6Laj1s0oOrAyoy/saZJAaom801Rpqy88IaDZGhkhd65e";

    @PostMapping("/trigger-cleaning")
    public ResponseEntity<String> triggerCleaning(@RequestParam String jobID, @RequestHeader("Authorization") String token) {
        return triggerCleaningService.triggerCleaning(jobID);
    }
}