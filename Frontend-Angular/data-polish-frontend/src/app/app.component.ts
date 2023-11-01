import { Location } from '@angular/common';
import { Component, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { MenuItem,MessageService  } from 'primeng/api';
import { AccessibilityServiceService } from './Services/accessibility/accessibility-service.service';
import { TerminalService } from 'primeng/terminal';
import { Subscription } from 'rxjs';
import { InputType } from '@coreui/angular';
import { BlobStorageService } from './Services/Fileupload/blob-storage.service';
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
  subscription: Subscription | undefined;
  constructor( private location: Location,
     private router: Router,
     private messageService :MessageService,
     private cookieService: CookieService,
     private accessibilityServiceService:AccessibilityServiceService,
     private terminalService:TerminalService,
     private BlobStorageService:BlobStorageService
  ){

    this.subscription = this.terminalService.commandHandler.subscribe((command) => {
      this.terminalhandler(command);
     
  });
  }
  ngOnInit() {
    let cookieValue:string = this.cookieService.get('ACCESSIBILITY');
    if(cookieValue!='' && cookieValue!="DEFAULT"){
      this.accessibilityset();
   }

}
accessibilityset(){
  if(this.cookieService.get('ACCESSIBILITY')=="DEFAULT"){
    alert('Please reload the page to set theme');
  }else{
    this.navclass='nav-2';
    this.accessibilityServiceService.basicsetting();
  }
  
      

}
  navigate(e:any){
    this.router.navigate([e]);
      
  }

  sidebarVisible: boolean = false;
  showsidebar(){
    this.sidebarVisible=true;
  }
  changeBG(color:any){    
    this.cookieService.set('ACCESSIBILITY',color);
    this.accessibilityset();
  }
  

  adhdmodal=false;
  adhfilename:any = null; 

adhd(){
this.adhdmodal=true;
}
terminalhandler(cmd:any){
  cmd=cmd.toUpperCase();
 if(cmd=="UPLOAD"){
    document.getElementById('uploadadhd')?.click();
    this.terminalService.sendResponse('File has been selected. use profile command to upload to cloud and start data profile');
  }
  if(cmd=="Profile"){
   this.BlobStorageService.uploadtoBlob(this.adhfilename).subscribe((e)=>{
    console.log(e);
   });
  }

 
}
adhdfile(e:any){
  this.adhfilename=e.target.files[0];
  console.log(this.adhfilename)
}

 
}
