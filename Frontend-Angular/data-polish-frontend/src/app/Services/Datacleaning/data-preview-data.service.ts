import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class DataPreviewDataService {

  constructor(private HttpClient:HttpClient) { }


  public getData(){
    return this.HttpClient.get("http://localhost:3000/getdatapreviewdata1");

  }
}
