import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class AccessibilityServiceService {

  constructor(private cookieService: CookieService
    ) { }
  basicsetting(){
  
    var bg=this.cookieService.get('ACCESSIBILITY');
    if(bg!='DEFAULT'){
      document.body.style.backgroundImage='none';
      document.body.style.backgroundColor = bg;
    }
    if(bg=='BLUE'){
      // document.body.style.color='yellow'
    }
    var glasscard:any= document.getElementsByClassName("glass-card");
      for (var i = 0; i < glasscard.length; i++) {
       glasscard[i].classList.add("no-glass-card");
        glasscard[i].classList.remove("glass-card");
      }
  }
}
