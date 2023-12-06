import { Injectable } from '@angular/core';
import { HttpClient,HttpParams,HttpHeaders } from '@angular/common/http';
import { AppSettings } from 'src/app/Const/config';
@Injectable({
  providedIn: 'root'
})
export class DataCleaningService {

  constructor(private HttpClient:HttpClient) { }
  public saveData(datarules:any,jobid:any){
    var URL=AppSettings.getBaseURL()+'data-clean?jobID='+jobid;
    return this.HttpClient.post(URL,datarules)
  }
}
