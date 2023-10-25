import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class AccessibilityServiceService {

  constructor(private cookieService: CookieService
    ) { }
  basicsetting(){
    var glasscard:any= document.getElementsByClassName("glass-card");
      this.cookieService.set('ACCESSIBILITY','TRUE');
      for (var i = 0; i < glasscard.length; i++) {
       glasscard[i].classList.add("no-glass-card");
        glasscard[i].classList.remove("glass-card");
      }
  }
}
