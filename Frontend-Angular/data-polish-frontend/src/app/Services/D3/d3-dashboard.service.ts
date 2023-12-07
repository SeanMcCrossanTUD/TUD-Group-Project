import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Observable, catchError, map, of, switchMap, throwError } from 'rxjs';
import { AppSettings } from 'src/app/Const/config';

@Injectable({
  providedIn: 'root'
})
export class D3DashboardService {

  constructor(private http: HttpClient,
    private cookieService: CookieService) { }
    static data:any;
   static currentjobid='';
    static data2:any;
    static qualityMetricsDate:any;
    static bubbleChartData:any
   getData(): Observable<any> {
    const jobID = this.cookieService.get('jobsid');
    if(jobID!=D3DashboardService.currentjobid){
      D3DashboardService.data=null;
    }
    if (D3DashboardService.data) {
      // If data is already available, return it as an observable
      return of(D3DashboardService.data);
    } else {
      // If data is not available, fetch it from the API

      const URL = `${AppSettings.getBaseURL()}data-profile`;
      let params = new HttpParams();
      params = params.append('jobID', jobID);
    
  
       return this.http.get(URL, { params: params,responseType:'text'}).pipe(
        switchMap((r1) => {
          
          return this.http.get<any>(`https://fab5storage.blob.core.windows.net/dataprofileoutput/${r1}`).pipe(
            map((result) => {
           
              D3DashboardService.data = result;
              D3DashboardService.currentjobid=jobID;
              return result;
            }),
            catchError((error) => {
              console.error('Error fetching data:', error);
              return of(null); // You can handle the error as needed
            })
          );
        })
      );
    }
  }

  getoutlier(): Observable<any> {
    const jobID = this.cookieService.get('jobsid');
    const url = `https://fab5storage.blob.core.windows.net/outlier/data_quality_result_outlier_${jobID}.json`;
    if(jobID!=D3DashboardService.currentjobid){
      D3DashboardService.data=null;
    }
    if (D3DashboardService.data2) {
      // If data is already available, return it as an observable
      return of(D3DashboardService.data2);
    } else {
    return this.http.get(url).pipe(
      map((res: any) =>{
        return res;
      }),
      catchError((error) => {
        console.error('Error fetching outlier data:', error);
        return throwError('Something went wrong while fetching outlier data.'); // You can customize the error message
      })
    );
    }
  }


  getQualityMertic(): Observable<any>{

    const jobID = this.cookieService.get('jobsid');
    const url = `https://fab5storage.blob.core.windows.net/qualityscore/data_quality_result_qualityscore_${jobID}.json`;
    if(jobID!=D3DashboardService.currentjobid){
      D3DashboardService.qualityMetricsDate=null;
    }
    if (D3DashboardService.qualityMetricsDate) {
      return of(D3DashboardService.qualityMetricsDate);
    } else {
    return this.http.get(url).pipe(
      map((res: any) =>{
      
        D3DashboardService.currentjobid=jobID;
        D3DashboardService.qualityMetricsDate=res;
        return res;
      }),
      catchError((error) => {
        console.error('Error fetching outlier data:', error);
        return throwError('Something went wrong while fetching outlier data.'); // You can customize the error message
      })
    );
    }
   
  }

  
  getBubbleChart(): Observable<any>{

    const jobID = this.cookieService.get('jobsid');
   
    const url = `https://fab5storage.blob.core.windows.net/bubblechart/data_quality_result_bubblechart_${jobID}.json`;
    if(jobID!=D3DashboardService.currentjobid){
      D3DashboardService.bubbleChartData=null;
    }
    if (D3DashboardService.bubbleChartData) {
      return of(D3DashboardService.bubbleChartData);
    } else {
    return this.http.get(url).pipe(
      map((res: any) =>{
      
        D3DashboardService.currentjobid=jobID;
        D3DashboardService.bubbleChartData=res;
        return res;
      }),
      catchError((error) => {
        console.error('Error fetching outlier data:', error);
        return throwError('Something went wrong while fetching outlier data.'); // You can customize the error message
      })
    );
    }
   
  }
    


  
}
