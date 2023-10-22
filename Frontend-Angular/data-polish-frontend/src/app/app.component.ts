import { Location } from '@angular/common';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { MenuItem,MessageService  } from 'primeng/api';


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
     private messageService :MessageService  ){}

  ngOnInit() {
 
}
  navigate(e:any){
    this.router.navigate([e]);
      
  }

  sidebarVisible: boolean = false;
  showsidebar(){
    this.sidebarVisible=true;
  }
  blackwhite(){
    this.navclass='nav-2'
    document.body.style.backgroundColor = "black";
    document.body.style.backgroundImage='none';
  }

 
}
