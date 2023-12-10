package com.example.Data.PolishBackend.Controller;

import com.example.Data.PolishBackend.Service.SetPasswordService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@CrossOrigin(origins = {"http://16.170.150.247:9000", "http://localhost:4200"})

public class SetPasswordController {

    @Autowired
    private SetPasswordService setPasswordService;

    @GetMapping("/set-password")
    public ResponseEntity<String> registerUser(
            @RequestParam String email,
            @RequestParam String otp,
            @RequestParam String newPassword
    ) {
        return setPasswordService.setPassword(email,otp,newPassword);
    }
}