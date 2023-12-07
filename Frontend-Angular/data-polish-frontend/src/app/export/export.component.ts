import { Component } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { AccessibilityServiceService } from '../Services/accessibility/accessibility-service.service';
import { FileExportService } from '../Services/fileExport/file-export.service';
import { fadeInAnimation } from '../Animations/animation';
import { HttpClient } from '@angular/common/http';
import { AppSettings } from '../Const/config';
import { saveAs } from 'file-saver';
import { MessageService } from 'primeng/api';
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
  private http: HttpClient,
  private messageService: MessageService

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
       
      },
      (error:any)=>{
        if(error.status==500){
          this.messageService.add({ severity: 'error', summary: 'Data Not Cleaned Yet', detail: 'Your data is till under cleaning' });
        }
  
      }
    )


  }

}
