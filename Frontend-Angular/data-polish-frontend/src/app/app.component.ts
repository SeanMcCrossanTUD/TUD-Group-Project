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
declare var LeaderLine: any;
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  
  currentpage=1;
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
  line1active:any
  line2active:any
  line3active:any
  line1:any
  line2:any
  line3:any
  
  ngOnInit() {
    let cookieValue:string = this.cookieService.get('ACCESSIBILITY');
    if(cookieValue!='' && cookieValue!="DEFAULT"){
      this.accessibilityset();
   }


   const div1 = document.querySelector('#div-1');
   const div2 = document.querySelector('#div-2');
   const div3 = document.querySelector('#div-3');
   const div4 = document.querySelector('#div-4');
//    startSocketGravity: [0, 0],
// endSocketGravity: [-192, -172]
this.line1 = new LeaderLine(div1, div2,{color:'white',hide:true})
this.line2 = new LeaderLine(div2, div3,{color:'white',hide:true})
this.line3 = new LeaderLine(div3, div4,{color:'white',hide:true})
this.line1active = new LeaderLine(div1, div2,{color:'white',dash: {animation: true}})
this.line2active = new LeaderLine(div2, div3,{color:'white',dash: {animation: true},hide:true})
this.line3active = new LeaderLine(div3, div4,{color:'white',dash: {animation: true},hide:true})

}
toggleLine(line:any){
  if(line==11){
    this.line1.hide();
    this.line1active.show();
  }
  if(line==12){
    this.line1.show();
    this.line1active.hide();
  }
  if(line==13){
    this.line1.hide();
    this.line1active.hide();
  }
  if(line==21){

    this.line2.hide();
    this.line2active.show();
  }
  if(line==22){
    this.line2.show();
    this.line2active.hide();
  }
  if(line==23){
    this.line2.hide();
    this.line2active.hide();
  }
  if(line==31){
    
    this.line3.hide();
    this.line3active.show();
  }
  if(line==32){
    this.line3.show();
    this.line3active.hide();
  }
  if(line==33){
    this.line3.hide();
    this.line3active.hide();
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





/******** */
backStyle='visibility: collapse;'
nextStyle='visibility: visible;'
movenext(){
  if(this.currentpage<4){
    this.currentpage++;
    this.router.navigate([this.currentpage]);
    if(this.currentpage==2){
      this.toggleLine(12);
      this.toggleLine(21);
    }
    if(this.currentpage==3){
      this.toggleLine(22);
      this.toggleLine(31);
    }
    if(this.currentpage==3){
      this.toggleLine(31);

    }
    if(this.currentpage==4){
      this.toggleLine(32);

    }
    if(this.currentpage!=1){
      this.backStyle='visibility: visible;'
    }
    if(this.currentpage==4){
      this.nextStyle='visibility: collapse;'
    }
    
  }
  
 
}
moveback(){
  if(this.currentpage>1){
    this.currentpage--;
    this.router.navigate([this.currentpage]);
    if(this.currentpage==1){
      this.backStyle='visibility: collapse;'
    }
    if(this.currentpage!=4){
      this.nextStyle='visibility: visible;'
    }

    if(this.currentpage==3){
      this.toggleLine(31);
    }
    if(this.currentpage==2){
      this.toggleLine(21);
      this.toggleLine(33);
    }
    if(this.currentpage==1){
      this.toggleLine(23);
      this.toggleLine(11)
    }
  }
 
}
 
}
