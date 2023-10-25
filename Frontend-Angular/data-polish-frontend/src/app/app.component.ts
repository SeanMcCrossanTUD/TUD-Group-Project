import { Location } from '@angular/common';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { MenuItem,MessageService  } from 'primeng/api';
import { AccessibilityServiceService } from './Services/accessibility/accessibility-service.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'dataPolish';
  items: any | null;
  radius:any =100;
  navclass='nav';
  constructor( private location: Location,
     private router: Router,
     private messageService :MessageService,
     private cookieService: CookieService,
     private accessibilityServiceService:AccessibilityServiceService
  ){}
  ngOnInit() {
    let cookieValue:string = this.cookieService.get('ACCESSIBILITY');
    if(cookieValue=='TRUE'){
      this.accessibilityset();
   }

}
accessibilityset(){
  this.navclass='nav-2';
  this.accessibilityServiceService.basicsetting();
      

}
  navigate(e:any){
    this.router.navigate([e]);
      
  }

  sidebarVisible: boolean = false;
  showsidebar(){
    this.sidebarVisible=true;
  }
  blackwhite(){
    this.accessibilityset();
    document.body.style.backgroundColor = "black";
    document.body.style.backgroundImage='none';
  
  }

  changeOpenDyslexicFont(){
    alert('hi')
    document.body.style.fontFamily="OpenDyslexic";
  }

 
}
