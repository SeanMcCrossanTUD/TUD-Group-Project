package com.example.Data.PolishBackend;


import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class home {
    @RequestMapping("/")
    public String msg() {
        return "Welcome to Data Polish!";
    }
}
