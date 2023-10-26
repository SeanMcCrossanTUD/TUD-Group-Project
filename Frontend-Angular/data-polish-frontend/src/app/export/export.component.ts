import { Component } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { AccessibilityServiceService } from '../Services/accessibility/accessibility-service.service';

@Component({
  selector: 'app-export',
  templateUrl: './export.component.html',
  styleUrls: ['./export.component.css']
})
export class ExportComponent {
  checkStatusString='';
constructor(
  private cookieService: CookieService,
  private accessibilityServiceService: AccessibilityServiceService
  ){}
  ngOnInit() {
    let cookieValue: string = this.cookieService.get('ACCESSIBILITY');
    if (cookieValue != '' && cookieValue != 'DEFAULT') {
      this.accessibilityServiceService.basicsetting();
    }
  }
  checkStatus(e:any){
    this.checkStatusString=e;
    console.log(e);
  }
  checkstatusbutton(){
    alert('you Data has been cleaned...');
  }
  download(){
   
    // var url="https://fab5storage.blob.core.windows.net/flaskapi2output/clean_data_1697040726.csv"
    // window.open(url);
  }
}
