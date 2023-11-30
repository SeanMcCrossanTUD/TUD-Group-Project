import { Injectable } from '@angular/core';
import { HttpClient,HttpParams,HttpHeaders } from '@angular/common/http';
import { AppSettings } from 'src/app/Const/config';
@Injectable({
  providedIn: 'root'
})
export class DataPreviewDataService {

  constructor(private HttpClient:HttpClient) { }


  public getData(jobid:any){

   
    var x=AppSettings.getBaseURL()+'data-preview';
    let params = new HttpParams();

    params = params.append('jobID', jobid)
    return this.HttpClient.get(x, {params:params,responseType: 'text'},) 
  }

  public getJsonData(x:any){
    return this.HttpClient.get('https://fab5storage.blob.core.windows.net/datapreview/'+x
    )
  }
  public getJsonData2(x:any){
    return this.HttpClient.get('http://localhost:3000/getdatapreviewdata1');
    
  }
}
