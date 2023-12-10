package com.example.Data.PolishBackend.Service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Random;

/*
* take email from frontend
* generate a random 4 digit otp
* encode the otp and insert into 'users' table for the email
* return the unencrypted OTP
*  */

@Service
public class ForgetPasswordService {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

}
