import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http'
@Injectable({
  providedIn: 'root'
})
export class BlobStorageService {

  constructor(private http:HttpClient) { }
  uploadtoBlob(x:any){
  
    let testData:FormData = new FormData();
    //testData.append("file",x.file)
    testData.append("name",x.name)
    var json=JSON.stringify(testData)
    const logicappsURI="https://prod-13.germanywestcentral.logic.azure.com:443/workflows/589549e32d5a40dda3b1437d090e6258/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=bIbHs51G_SNDQNLgur5RDdSjY_adWhSRM58uf6LNoA0";
    this.http.post(logicappsURI,json).subscribe((respose)=>{
      alert("done");
    })
  }
}
