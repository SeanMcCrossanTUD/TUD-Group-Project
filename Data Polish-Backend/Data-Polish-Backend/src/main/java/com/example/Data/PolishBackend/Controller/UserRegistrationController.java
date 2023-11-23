package com.example.Data.PolishBackend.Controller;

import com.example.Data.PolishBackend.Service.UserRegistrationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@CrossOrigin(origins = {"http://16.170.150.247:9000", "http://localhost:4200"})
@RequestMapping("/api/register")
public class UserRegistrationController {

    @Autowired
    private UserRegistrationService userRegistrationService;

    @PostMapping
    public ResponseEntity<String> registerUser(
            @RequestBody String fullName,
            @RequestBody String email,
            @RequestBody String password
    ) {
        userRegistrationService.registerUser(fullName, email, password);
        return new ResponseEntity<>("New user successfully created", HttpStatus.CREATED);
    }
}
