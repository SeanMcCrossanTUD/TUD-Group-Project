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
import { fadeInAnimation } from './Animations/animation';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  
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
  ){ }
  line1active:any
  line2active:any
  line3active:any
  line4active:any
  line1:any
  line2:any
  line3:any
  line4:any
  linecolor:any='white';
  ngOnInit() {
    let login:string = this.cookieService.get('LOGIN');
    if(login=='TRUE'){
      this.isLoggedin = true;
    }

      let cookieValue: string = this.cookieService.get('ACCESSIBILITY');
      if (cookieValue != '' && cookieValue != 'DEFAULT') {
        this.accessibilityset();
      }

      if(cookieValue=='BLUE'){
        this.linecolor='yellow'
      }else if(cookieValue=='WHEAT'){    
        this.linecolor='black'
      }else if(cookieValue=='BLACK'){
        this.linecolor='white'
      }

    

  //}


}

ngAfterViewInit(){
  try{
  const div1 = document.querySelector('#div-1');
      const div2 = document.querySelector('#div-2');
      const div3 = document.querySelector('#div-3');
      const div4 = document.querySelector('#div-4');
      const div5 = document.querySelector('#div-5');
      const linecolor = this.linecolor;
      this.line1 = new LeaderLine(div1, div2, { color: linecolor, hide: true });
      this.line2 = new LeaderLine(div2, div3, { color: linecolor, hide: true });
      this.line3 = new LeaderLine(div3, div4, { color: linecolor, hide: true });
      this.line4 = new LeaderLine(div4, div5, { color: linecolor, hide: true });
      this.line1active = new LeaderLine(div1, div2, {
        color: linecolor,
        dash: { animation: true },
      });
      this.line2active = new LeaderLine(div2, div3, {
        color: linecolor,
        dash: { animation: true },
        hide: true,
      });
      this.line3active = new LeaderLine(div3, div4, {
        color: linecolor,
        dash: { animation: true },
        hide: true,
      });
      this.line4active = new LeaderLine(div4, div5, {
        color: linecolor,
        dash: { animation: true },
        hide: true,
      });
    }catch{}
}
toggleLine(line:any){
  if(line==11){
    this.line1.hide();
    this.line1active.show();
  }
  if(line==12){
    this.line1.show('draw', {
      animOptions: {
        duration: 3000,
        timing: [0.5, 0, 1, 0.42]
      }});
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
    this.line2.show('draw', {
      animOptions: {
        duration: 3000,
        timing: [0.5, 0, 1, 0.42]
      }});
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
    this.line3.show('draw', {
      animOptions: {
        duration: 3000,
        timing: [0.5, 0, 1, 0.42]
      }});;
    this.line3active.hide();
  }
  if(line==33){
    this.line3.hide();
    this.line3active.hide();
  }
  if(line==41){
    
    this.line4.hide();
    this.line4active.show();
  }
  if(line==42){
    this.line4.show('draw', {
      animOptions: {
        duration: 3000,
        timing: [0.5, 0, 1, 0.42]
      }});;
    this.line4active.hide();
  }
  if(line==43){
    this.line4.hide();
    this.line4active.hide();
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
  






/******** */
backStyle='visibility: collapse;'
nextStyle='visibility: visible;'
movenext(){
  if(this.currentpage<5){
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
      this.toggleLine(41);

    }
    if(this.currentpage==5){
     
      this.toggleLine(42);
    }
    if(this.currentpage!=1){
      this.backStyle='visibility: visible;'
    }
    if(this.currentpage==5){
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
    if(this.currentpage!=5){
      this.nextStyle='visibility: visible;'
    }
    if(this.currentpage==4){
      this.toggleLine(41);
    }
    if(this.currentpage==3){
      this.toggleLine(31);
      this.toggleLine(43);
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

  tooltipItems!: MenuItem[] | null;

  color='red'
  setcolor(){
    this.cookieService.set('ACCESSIBILITY',this.color);
    this.accessibilityset(); 
  }


  chart_primary_color='lightblue'
  set_chart_primary_color(){
    this.cookieService.set('chartprimarycolor',this.chart_primary_color);
    this.applytocharts("bar-1");
    this.applytocharts("dot");
   
  }
  applytocharts( x:any){
    var elements:any= document.getElementsByClassName(x)
   for(var i=0;i<elements.length;i++){
    elements[i].style="fill:"+this.chart_primary_color+";"
   }
  }

  isLoggedin=false;
  emailid:any=''
  password:any=''

  logInInToSystem(){
  
    var regex=/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
   
 
    if(this.emailid!='' &&
     this.emailid!=undefined 
      && regex.test(this.emailid)
      && this.password!='' &&
       this.password!=undefined
    )
    {

      this.isLoggedin=true;
      this.cookieService.set('LOGIN','TRUE')
      
    }else{
      this.messageService.add({ severity: 'error', 
      summary: 'something went wrong  ',
    detail:'check your credientials' })
    }
  }

  logout(){
    this.isLoggedin=false;
    this.cookieService.set('LOGIN','FALSE')
  }
}

