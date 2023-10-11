package com.datapolish.Data.Polish.Backend;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class hi {
    @RequestMapping("/")
    public String msg() {
        return "Welcome to Data Polish!";
    }
}
