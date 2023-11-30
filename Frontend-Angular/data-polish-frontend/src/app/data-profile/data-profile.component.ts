import { Component ,ViewChild} from '@angular/core';
import { MenuItem } from 'primeng/api';
import { CookieService } from 'ngx-cookie-service';
import { AccessibilityServiceService } from '../Services/accessibility/accessibility-service.service';
import { FileExportService } from '../Services/fileExport/file-export.service';
import { fadeInAnimation } from '../Animations/animation';
import { DataProfileConfig } from '../Const/Dataprofile_config';
@Component({
  selector: 'app-data-profile',
  templateUrl: './data-profile.component.html',
  styleUrls: ['./data-profile.component.css'],
  animations: [fadeInAnimation],
  host: { '[@fadeInAnimation]': '' }
})
export class DataProfileComponent {
  visible: boolean = false;
  items: MenuItem[] | undefined;
  @ViewChild('img') img!: any;
  @ViewChild('newwindow') newwindow!:any;
  seeimage(e:any){

   window.open(e);

   

  }
  imgURL=""
  header=""
  showDialog(e:any,c:any) {
    // if(this.foldername==''){
    //   alert("your data is not Profiled yet");
    // }else{
    //   let baseurl='https://fab5storage.blob.core.windows.net/imagesoutput/'+this.foldername+'/';
    //   this.imgURL=baseurl+e;
    //   this.header=c;
     
    // }
    this.visible = true;
}

constructor(
  private cookieService: CookieService,
  private accessibilityServiceService: AccessibilityServiceService,
  private fileExportService:FileExportService,
 
  ){}

jobid=''
ngOnInit() {

  this.jobid=this.cookieService.get('jobsid');
 
  
  let cookieValue: string = this.cookieService.get('ACCESSIBILITY');
  if (cookieValue != '' && cookieValue != 'DEFAULT') {
    this.accessibilityServiceService.basicsetting();
  }

}




checkStatusString=''
foldername='';
checkstatusbutton(){

  
}

hide_more=true

showMore(){
  
  this.hide_more=!this.hide_more
}

/// help text
WHAT:any;
WHY:any;
visibleHelpText=false;
openHelpText(element:any){
  console.log(DataProfileConfig.NUMBEROFFIELDS)
  this.visibleHelpText=true;
  
}
}
