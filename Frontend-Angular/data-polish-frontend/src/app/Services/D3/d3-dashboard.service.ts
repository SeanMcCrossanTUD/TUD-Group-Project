import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, map, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class D3DashboardService {

  constructor(private http: HttpClient) { }
   data:any;

   getData(): Observable<any> {
    var apiurl='assets/data_quality_result.json';
    if (this.data) {
      // If data is already available, return it as an observable
      return of(this.data);
    } else {
      // If data is not available, fetch it from the API
      return this.http.get<any>(apiurl).pipe(
        map((result) => {
          this.data = result;
          return result;
        }),
        catchError((error) => {
          console.error('Error fetching data:', error);
          return of(null); // You can handle the error as needed
        })
      );
    }
  }
    


  
}
