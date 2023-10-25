import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { AccessibilityServiceService } from '../Services/accessibility/accessibility-service.service';
@Component({
  selector: 'app-data-cleaning',
  templateUrl: './data-cleaning.component.html',
  styleUrls: ['./data-cleaning.component.css']
})
export class DataCleaningComponent {
  constructor(
    private router: Router,
    private cookieService: CookieService,
    private accessibilityServiceService: AccessibilityServiceService
    ){

  }
  ngOnInit() {
    let cookieValue: string = this.cookieService.get('ACCESSIBILITY');
    if (cookieValue != '' && cookieValue != 'DEFAULT') {
      this.accessibilityServiceService.basicsetting();
    }
  }
  StartCleaning(){
    alert("data cleaning is started...");
    this.router.navigate(["/Export"]);

  }
}
