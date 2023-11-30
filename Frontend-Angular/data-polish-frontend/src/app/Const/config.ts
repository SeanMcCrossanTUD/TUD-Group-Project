
import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { config } from 'rxjs';
export class AppSettings {
   
    public static getBaseURL(){
        try{
            // let x=window.location.href;
            // let y=x.split('v2');
            // return y[0];
            return 'http://localhost:8090/';
        }catch{
            return 'http://localhost:8082/';
        }
       
    }

}
@Injectable({
    providedIn: 'root'
  })
export class constants{
    constructor(private http:HttpClient){
        http.get('assets/Dataprofile_config.json').subscribe(
            (res)=>{
                this.config=res;
            },
            (err)=>{
                alert('erre');
                console.log(err);
            }
        )
    }
   config:any;
//   'EXAMPLE':'example'

}

