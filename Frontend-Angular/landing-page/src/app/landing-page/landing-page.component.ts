import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
@Component({
  selector: 'app-landing-page',  
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.css'
})
export class LandingPageComponent {
 
  constructor(private router:Router,
    private http:HttpClient){}
  openTutorial() {
    console.log('Opening tutorial...');
    // Add logic to navigate to the tutorial page or show a modal
  }

  getStarted() {
    // var url=window.location+'user-registration'
    // window.location.replace(url);
    this.router.navigate(["/user-registration"]);
    // Add logic to navigate to the get started page or perform other actions
  }
  openUserManual(){
    window.open('assets/user-manual.pdf','_blank')
    

  }
}
