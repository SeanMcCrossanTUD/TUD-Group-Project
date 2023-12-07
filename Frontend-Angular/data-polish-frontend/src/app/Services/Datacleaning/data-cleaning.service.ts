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
  public downLoadRules(jobid:any){
    var URL=AppSettings.getBaseURL()+'rules-export?jobID='+jobid;
    return this.HttpClient.get(URL,{responseType:'text'})
  }

  public downloadRulesFromBlob(blobName:any){
    var containerName='rules/'
    var url=AppSettings.getBlobURL()+containerName+blobName;
    return url;
  }

  public uploadRules(x:any){
    var URL=AppSettings.getBaseURL()+"rules-import";
    var formdata = new FormData();
    formdata.append("file", x, x.name)
    
    //var json=JSON.stringify(formdata)
      return this.HttpClient.post(URL,formdata);
  }
}
