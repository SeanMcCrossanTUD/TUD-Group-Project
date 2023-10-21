import { Location } from '@angular/common';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'dataPolish';
  constructor( private location: Location, private router: Router ){}
  navigate(e:any){
    this.router.navigate([e]);
       // this.location.replaceState(e);
  }

 
}
