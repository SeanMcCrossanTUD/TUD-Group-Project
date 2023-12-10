package com.example.Data.PolishBackend.Service;

/*
* take strings email, otp, password from frontend
* get value from 'password' column from 'users' table for the email and store it as string 'encodedOTP'
* decode the 'encodedOTP' value and match with otp from frontend
* if they match then hash the password taken from frontend and insert hashed password into 'password' column
* else return "OTP is invalid"
* */

public class SetPasswordService {
}
