import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http'
import {AppSettings} from '../../Const/config';
@Injectable({
  providedIn: 'root'
})
export class BlobStorageService {

  constructor(private http:HttpClient) { }
  uploadtoBlob(x:any){
    var URL=AppSettings.javaapiurl+"/upload-csv";
    var formdata = new FormData();
    formdata.append("file", x, x.name)
    
    //var json=JSON.stringify(formdata)
      return this.http.post(URL,formdata);
  }

  getOutputFileURL(x:any){
    var URL=AppSettings.javaapiurl+"/download";
    var formdata=new FormData();
    formdata.append('jobid',x);
    return this.http.post(URL,formdata);
  }

}
