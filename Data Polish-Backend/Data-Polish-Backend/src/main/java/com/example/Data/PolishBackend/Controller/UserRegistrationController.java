package com.example.Data.PolishBackend.Controller;

import com.example.Data.PolishBackend.Service.UserRegistrationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@CrossOrigin(origins = {"http://16.170.150.247:9000", "http://localhost:4200"})
//@RequestMapping("/user-register")
public class UserRegistrationController {

    @Autowired
    private UserRegistrationService userRegistrationService;

    @PostMapping("/user-register")
    public ResponseEntity<String> registerUser(
            @RequestParam String fullName,
            @RequestParam String email,
            @RequestParam String password
    ) {
        return userRegistrationService.registerUser(fullName, email, password);
    }
}
