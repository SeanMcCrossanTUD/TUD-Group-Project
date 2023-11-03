import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { AccessibilityServiceService } from '../Services/accessibility/accessibility-service.service';
import { FileExportService } from '../Services/fileExport/file-export.service';
@Component({
  selector: 'app-data-cleaning',
  templateUrl: './data-cleaning.component.html',
  styleUrls: ['./data-cleaning.component.css']
})
export class DataCleaningComponent {

  buttonstyle={'background-color':'#c3ebe1'}
  // # [style]="buttonstyle"
  constructor(
    private router: Router,
    private cookieService: CookieService,
    private accessibilityServiceService: AccessibilityServiceService,
    private fileExportService:FileExportService
    ){

  }
  
  ngOnInit() {
    this.checkStatusString=this.cookieService.get('jobsid');
    let cookieValue: string = this.cookieService.get('ACCESSIBILITY');
    if (cookieValue != '' && cookieValue != 'DEFAULT') {
      this.accessibilityServiceService.basicsetting();
    }
  }
  checkStatusString=''
  StartCleaning(){
    
    this.fileExportService.startDataCLeanning(this.checkStatusString).subscribe(
      (Response)=>{
        alert("data cleaning has started...");
      },
      (error)=>{
      
        alert("something went wrong check your id");
      }
    )
    // this.router.navigate(["/Export"]);

  }

  // 
}
