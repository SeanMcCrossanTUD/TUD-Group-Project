import { Component } from '@angular/core';
import { MessageService } from 'primeng/api';
import { CookieService } from 'ngx-cookie-service';
import { AccessibilityServiceService } from '../Services/accessibility/accessibility-service.service';
import { AppSettings } from '../Const/config';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css'],

})
export class HomePageComponent {
  jobids=[];
  constructor(
    private messageService: MessageService,
    private cookieService: CookieService,
    private accessibilityServiceService: AccessibilityServiceService,
   
  ) {}

  ngOnInit() {
    let cookieValue: string = this.cookieService.get('ACCESSIBILITY');
    if (cookieValue != '' && cookieValue != 'DEFAULT') {
      this.accessibilityServiceService.basicsetting();
    }

    try{
      this.jobids=JSON.parse(this.cookieService.get('jobsid'))
    }catch{}

   
  }

  copytoclipboard(e: any) {
    navigator.clipboard.writeText(e);
    this.messageService.add({ severity: 'success', summary: 'ID copied ' });

  }
}
