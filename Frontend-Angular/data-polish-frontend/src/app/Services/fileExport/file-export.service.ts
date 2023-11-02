import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http'
import {AppSettings} from '../../Const/config';
@Injectable({
  providedIn: 'root'
})
export class FileExportService {

  constructor(
    private http:HttpClient
    ) { }
 


  checkStatus(x:any){
    let url=AppSettings.getBaseURL()+'download-csv';
    let params = new HttpParams();
    params = params.append('jobID', x)
    return this.http.get(url,{params:params})
  }
  startDataCLeanning(x:any){
    let url=AppSettings.getBaseURL()+'data-clean';
    let params = new HttpParams();
    params = params.append('jobID', x)
    return this.http.get(url,{params:params})
  }


}
