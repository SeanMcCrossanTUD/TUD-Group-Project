import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DataPreviewDataService {

  constructor() { }

  mockData={
    "coloumnNames":['a','b'],
    "data":[
      {
        'a':123,
        'b':342
      }
    ]
  }

  public getData(){
    return this.mockData
  }
}
