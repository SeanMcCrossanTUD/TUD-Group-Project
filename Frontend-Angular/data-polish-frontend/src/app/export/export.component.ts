import { Component } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { AccessibilityServiceService } from '../Services/accessibility/accessibility-service.service';
import { FileExportService } from '../Services/fileExport/file-export.service';
import { fadeInAnimation } from '../Animations/animation';
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
  private fileExportService:FileExportService
  ){}
  ngOnInit() {
    this.checkStatusString=this.cookieService.get('jobsid');
    let cookieValue: string = this.cookieService.get('ACCESSIBILITY');
    if (cookieValue != '' && cookieValue != 'DEFAULT') {
      this.accessibilityServiceService.basicsetting();
    }
  }
  outputURI='';
  checkstatusbutton(){   
    
    this.fileExportService
    .checkStatus(this.checkStatusString)
    .subscribe((Response:any)=>{
     
      if(Response.datacleaningoutput=='null'){
        alert("your data is not cleaned yet");
      }else{
        alert("your Data has been cleaned");
        this.outputURI=Response.datacleaningoutput;
      }
    },
    (err)=>{
      alert("something went wrong checkyour JobID");
    });
  }


  download(){
   if(this.outputURI=='' || this.outputURI==undefined ){
      alert('Error check status first');

   }else{
    var url="https://fab5storage.blob.core.windows.net/flaskapi2output/"+this.outputURI;
    window.open(url);
   }
    
  }
}
