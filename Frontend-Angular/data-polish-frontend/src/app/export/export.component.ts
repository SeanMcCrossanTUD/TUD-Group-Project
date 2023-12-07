import { Component } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { AccessibilityServiceService } from '../Services/accessibility/accessibility-service.service';
import { FileExportService } from '../Services/fileExport/file-export.service';
import { fadeInAnimation } from '../Animations/animation';
import { HttpClient } from '@angular/common/http';
import { AppSettings } from '../Const/config';
import { saveAs } from 'file-saver';
@Component({
  selector: 'app-export',
  templateUrl: './export.component.html',
  styleUrls: ['./export.component.css'],
  animations: [fadeInAnimation],
  host: { '[@fadeInAnimation]': '' }
})
export class ExportComponent {
  checkStatusString='';
constructor(
  private cookieService: CookieService,
  private accessibilityServiceService: AccessibilityServiceService,
  private http: HttpClient 

  ){}
  ngOnInit() {
    let cookieValue: string = this.cookieService.get('ACCESSIBILITY');
    if (cookieValue != '' && cookieValue != 'DEFAULT') {
      this.accessibilityServiceService.basicsetting();
    }
  }


  

  exportOptions:any[]=[
    {types:'CSV'},
    {types:'Excel'}
  ]
  selectedExportOption= {types:'CSV'};

  export(){
    
    var jobID=this.cookieService.get('jobsid');
  
    const fileType = this.selectedExportOption.types === 'Excel' ? '.xlsx' : '.csv';

    this.http.get(AppSettings.getBaseURL()+'download-file?jobID='+jobID+"&fileType="+fileType,
    {responseType:'blob'}).subscribe(
      (res)=>{
        
        var today = new Date();
          const fileName = 'Export-'+today.getHours()+"-"+today.getMinutes() + fileType; 
          saveAs(res, fileName);
        console.log(res);
      },
      (error)=>{
        console.log(error);
      }
    )


  }

}
