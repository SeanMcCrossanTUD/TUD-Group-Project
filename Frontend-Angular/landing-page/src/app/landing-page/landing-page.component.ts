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
    window.open('assets/user-manual.pdf','_blank');
  }

  moveTOSection(){
    var x:any=document.getElementById("tutorial-section");
    x.scrollIntoView({behavior: 'smooth'});
  }
  moveToTop(){
    window.scrollTo({top: 0, behavior: 'smooth'});
  }

  navToMainApp(){
    window.location.href='http://16.170.150.247:9000/datapolish/#/1'
  }

  }

