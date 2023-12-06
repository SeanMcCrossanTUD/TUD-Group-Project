package com.example.Data.PolishBackend.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.http.ResponseEntity;
import com.example.Data.PolishBackend.Service.UserLoginService;
import java.io.IOException;


@RestController
public class UserLoginController {
    @Autowired
    private UserLoginService userLoginService;

    @GetMapping("/user-login")
    public ResponseEntity<String> loginUser(@RequestParam String email, @RequestParam String password){
        return userLoginService.loginUser(email,password);
    }
}


