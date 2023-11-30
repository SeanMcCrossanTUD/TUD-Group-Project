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

  ){}
  ngOnInit() {
    let cookieValue: string = this.cookieService.get('ACCESSIBILITY');
    if (cookieValue != '' && cookieValue != 'DEFAULT') {
      this.accessibilityServiceService.basicsetting();
    }
  }


  stateOptions: any[] = [{label: 'CSV', value: 'CSV'}, {label: 'Excel', value: 'EXCEL'}];

  value: string = 'off';

  export(){
    alert(this.value)
  }

}
