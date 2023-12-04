import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AppSettings } from 'src/app/Const/config';

@Injectable({
  providedIn: 'root'
})
export class LoginServiceService {

  constructor(
    private http:HttpClient
  ) { }

  login(email:any,password:any){
    var URL=AppSettings.getBaseURL()+'user-login?email='+email+'&password='+password

      return this.http.get(URL,{responseType:'text'})
  }
}
