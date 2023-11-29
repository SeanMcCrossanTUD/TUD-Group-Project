package com.example.Data.PolishBackend.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.http.ResponseEntity;
import com.example.Data.PolishBackend.Service.UserLoginService;
import java.io.IOException;


@RestController
@CrossOrigin(origins = {"http://16.170.150.247:9000", "http://localhost:4200"})
public class UserLoginController {
    @Autowired
    private UserLoginService userLoginService;

    @PostMapping("/user-login")
    public ResponseEntity<String> loginUser(@RequestParam String email, @RequestParam String password){
        return userLoginService.loginUser(email,password);
    }
}


